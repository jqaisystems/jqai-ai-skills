"""Compare normalized claims from selected documents; never fetch, edit or publish."""
import datetime
import json
import re
import sys
from urllib.parse import urlsplit


def commit(value):
    return isinstance(value, str) and re.fullmatch(r"(?:[0-9a-fA-F]{40}|[0-9a-fA-F]{64})", value)


def valid(field, v):
    if field == "count":
        return type(v) is int and v >= 0
    if not isinstance(v, str) or not v.strip():
        return False
    if field == "tag":
        return v.strip() == v
    if field == "commit":
        return bool(commit(v))
    if field == "state":
        return v in {"draft", "published", "prerelease"}
    if field == "url":
        try:
            url = urlsplit(v)
            return url.scheme in {"http", "https"} and bool(url.hostname) and url.username is None
        except ValueError:
            return False
    return False


def dated(value):
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return False
    try:
        datetime.date.fromisoformat(value)
        return True
    except ValueError:
        return False


def identity(r):
    verified = True
    for field, a, b in [("tag", "tag", "release_tag"), ("commit", "tag_commit", "release_commit")]:
        x, y = r.get(a), r.get(b)
        if not valid(field, x) or not valid(field, y):
            verified = False
        elif (x.lower() != y.lower() if field == "commit" else x != y):
            return "conflicts"
    return "matches" if verified and valid("state", r.get("state")) else "not verified"


def compare(row, r, anchor):
    field, value = row.get("field"), row.get("value")
    if field not in ("tag", "commit", "state", "count", "url", "link_status"):
        return "not verified"
    if row.get("scope") == "historical" and dated(row.get("as_of")):
        return "historical: retain"
    if row.get("scope") != "current" or anchor != "matches":
        return "not verified"
    if field == "link_status":
        return {"confirmed-present": "matches", "confirmed-missing": "conflicts"}.get(str(value), "not verified")
    expected = r.get("tag_commit" if field == "commit" else field)
    if not valid(field, expected) or not valid(field, value):
        return "not verified"
    if field == "commit":
        expected, value = expected.lower(), value.lower()
    return "matches" if value == expected else "conflicts"


def audit(pack):
    if not isinstance(pack, dict) or type(pack.get("version")) is not int or pack["version"] != 1:
        raise ValueError
    r, rows = pack.get("release"), pack.get("claims")
    if not isinstance(r, dict) or not isinstance(rows, list) or not all(isinstance(x, dict) for x in rows):
        raise ValueError
    anchor = identity(r)
    verdicts = [compare(x, r, anchor) for x in rows]
    states = [anchor, *verdicts]
    code = 1 if "conflicts" in states else 2 if not rows or "not verified" in states else 0
    return {"identity": anchor, "claims": [{"row": n, "result": v} for n, v in enumerate(verdicts, 1)]}, code


def unique_fields(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError
        result[key] = value
    return result


def main():
    try:
        raw = sys.stdin.buffer.read(1024 * 1024 + 1)
        if len(raw) > 1024 * 1024:
            raise ValueError
        result, code = audit(json.loads(raw, object_pairs_hook=unique_fields))
    except (ValueError, RecursionError, OSError):
        result, code = {"error": "invalid or oversized evidence pack"}, 2
    print(json.dumps(result))
    return code


if __name__ == "__main__":
    sys.exit(main())
