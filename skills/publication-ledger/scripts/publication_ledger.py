"""Render selected JSON evidence on stdin as a private, offline Markdown report."""
import datetime as dt
import json
import re
import sys
import unicodedata

LIMIT = 2 * 1024 * 1024
KEY = ("work_id", "edition", "destination")
RANK = {"scheduled": 0, "reported published": 1, "verified": 2}
NEXT = {
    "scheduled": "Check for a delivery observation for this edition and destination.",
    "reported published": "Request a verification reference for this reported delivery.",
    "no evidence supplied": "Ask for a matching observation; leave the outcome unknown.",
    "conflicting evidence": "Compare the cited observations and confirm delivery identity and sequence.",
}


class Invalid(ValueError):
    """Only emit controlled diagnostics, never the supplied values."""


def fields(obj, required, where, optional=()):
    if not isinstance(obj, dict) or not set(required) <= obj.keys() <= set(required) | set(optional):
        raise Invalid(f"{where}: missing or unexpected field")


def alias(s, where):
    if not isinstance(s, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", s):
        raise Invalid(f"{where}: use a short lowercase alias")
    return s


def unique(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise Invalid("duplicate JSON field")
        obj[key] = value
    return obj


def literal(title):
    # Prevent Markdown interpretation, including hostile table separators/backticks.
    fence = chr(96) * (1 + max((len(x) for x in re.findall(chr(96) + "+", title)), default=0))
    return fence + " " + title.replace("|", r"\|") + " " + fence


def timestamp(s, where):
    if not isinstance(s, str) or not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:Z|[+-](?:[01]\d|2[0-3]):[0-5]\d)", s):
        raise Invalid(f"{where}: use an offset-aware timestamp")
    try:
        return dt.datetime.fromisoformat(s).astimezone(dt.timezone.utc)
    except (ValueError, OverflowError):
        raise Invalid(f"{where}: invalid calendar time") from None


def state(events):
    if not events:
        return "no evidence supplied"
    identities = {delivery for _, _, _, delivery in events if delivery}
    if len(identities) > 1 or any(kind == "disputed" for _, kind, _, _ in events):
        return "conflicting evidence"
    # Different stages at one instant have no established order.
    highest = -1
    stages = {}
    for when, kind, _, _ in events:
        stages.setdefault(when, set()).add(RANK[kind])
    for when in sorted(stages):
        if len(stages[when]) != 1 or min(stages[when]) < highest:
            return "conflicting evidence"
        highest = max(stages[when])
    return ("scheduled", "reported published", "verified")[highest]


def render(pack):
    fields(pack, ("version", "inventory", "observations"), "pack")
    if type(pack["version"]) is not int or pack["version"] != 1:
        raise Invalid("unsupported version")
    for name in ("inventory", "observations"):
        if not isinstance(pack[name], list):
            raise Invalid(f"{name}: expected a list")
    if not pack["inventory"]:
        raise Invalid("inventory: supply at least one row")
    rows, projects = {}, {}
    for n, row in enumerate(pack["inventory"], 1):
        where = f"inventory row {n}"
        fields(row, (*KEY, "project", "title"), where)
        key = tuple(alias(row[k], where) for k in KEY)
        project = alias(row["project"], where)
        if projects.setdefault(key[0], project) != project:
            raise Invalid(f"{where}: work ID belongs to another project")
        title = row["title"]
        if (not isinstance(title, str) or not 1 <= len(title) <= 160 or title != title.strip()
                or not title.isprintable() or any(unicodedata.category(c).startswith("C") for c in title)):
            raise Invalid(f"{where}: expected a short single-line display title")
        if key in rows:
            raise Invalid(f"{where}: duplicate inventory identity")
        rows[key] = (title, [])
    for n, obs in enumerate(pack["observations"], 1):
        where = f"observation {n}"
        fields(obs, (*KEY, "at", "kind", "ref"), where, ("delivery_id",))
        key = tuple(alias(obs[k], where) for k in KEY)
        if key not in rows:
            raise Invalid(f"{where}: no exact inventory row")
        kind = obs["kind"]
        if not isinstance(kind, str) or kind not in (*RANK, "disputed"):
            raise Invalid(f"{where}: unknown observation kind")
        ref = alias(obs["ref"], where)
        delivery = alias(obs["delivery_id"], where) if "delivery_id" in obs else ""
        rows[key][1].append((timestamp(obs["at"], where), kind, ref, delivery))

    history = ["# Publication history", "", "Supplied evidence only; no live verification."]
    queue = []
    last = None
    for work, edition, dest in sorted(rows, key=lambda k: (projects[k[0]], k[0], k[2], k[1])):
        title, events = rows[work, edition, dest]
        if work != last:
            history.extend(["", f"## {projects[work]} / {work}", "",
                            "| Destination | Edition | Title | Status | Observations (UTC) |",
                            "|---|---|---|---|---|"])
            last = work
        status = state(events)
        items = [f"{at:%Y-%m-%d %H:%M:%S} {kind} [{ref}]" + (f" (delivery: {d})" if d else "")
                 for at, kind, ref, d in sorted(events)]
        history.append(f"| {dest} | {edition} | {literal(title)} | {status} | " + "; ".join(items or ["None supplied"]) + " |")
        if status in NEXT:
            queue.append(f"| {work} | {edition} | {dest} | {status} | {NEXT[status]} |")
    review = ["# Review queue", ""]
    review.extend(["| Work ID | Edition | Destination | Status | Next check |", "|---|---|---|---|---|", *queue]
                  if queue else ["No unresolved rows in the supplied inventory."])
    return "\n".join([*history, "", *review])


def main():
    try:
        raw = sys.stdin.buffer.read(LIMIT + 1)
        if len(raw) > LIMIT:
            raise Invalid("pack exceeds 2 MiB")
        report = render(json.loads(raw.decode("utf-8-sig"), object_pairs_hook=unique))
    except Invalid as e:
        print(f"Invalid input: {e}.", file=sys.stderr)
        return 2
    except (ValueError, RecursionError, OSError):
        print("Invalid or unreadable JSON input.", file=sys.stderr)
        return 2
    sys.stdout.buffer.write((report + "\n").encode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
