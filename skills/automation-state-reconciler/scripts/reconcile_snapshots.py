#!/usr/bin/env python3
"""Compare offline snapshots without opening services or changing input records."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import sys

STATES = ("unchanged", "new", "changed", "duplicate", "missing-from-source", "ambiguous")
PROTECTED = {"scheduled", "published", "verified"}


def timestamp(value):
    if not isinstance(value, str):
        raise ValueError("Timestamps must be ISO 8601 strings with a timezone")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("Invalid ISO 8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise ValueError("Timestamps require a timezone")
    return parsed.astimezone(timezone.utc)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def read_json(path):
    if str(path).startswith(("\\\\", "//")):
        raise ValueError("Snapshots must be local files")
    path = path.expanduser().absolute()
    for item in (path, *path.parents):
        if item.is_symlink() or (item.exists() and getattr(item.lstat(), "st_file_attributes", 0) & 0x400):
            raise ValueError("Linked snapshot paths are not supported")
    def pairs(items):
        obj = {}
        for key, value in items:
            if key in obj:
                raise ValueError("Repeated JSON object key")
            obj[key] = value
        return obj
    return json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=pairs,
                      parse_constant=lambda _: (_ for _ in ()).throw(ValueError("Nonfinite JSON value")))


def validate_snapshot(data, now):
    required = {"schema_version", "captured_at", "complete", "max_age_hours", "compare_fields", "records"}
    if not isinstance(data, dict) or set(data) != required or type(data["schema_version"]) is not int or data["schema_version"] != 1:
        raise ValueError("Snapshot keys must match the version 1 contract")
    captured = timestamp(data["captured_at"])
    maximum = data["max_age_hours"]
    if isinstance(maximum, bool) or not isinstance(maximum, (int, float)) or not math.isfinite(maximum) or maximum <= 0:
        raise ValueError("max_age_hours must be positive and finite")
    if type(data["complete"]) is not bool:
        raise ValueError("complete must be boolean")
    fields = data["compare_fields"]
    if not isinstance(fields, list) or not fields or any(not isinstance(f, str) or not f for f in fields) or len(fields) != len(set(fields)):
        raise ValueError("compare_fields must be unique nonempty top-level field names")
    if not isinstance(data["records"], list):
        raise ValueError("records must be a list")
    indexed = defaultdict(list)
    for record in data["records"]:
        if not isinstance(record, dict) or set(record) - {"id", "values", "content_hash"}:
            raise ValueError("Invalid record keys")
        if not isinstance(record.get("id"), str) or not record["id"].strip() or not isinstance(record.get("values"), dict):
            raise ValueError("Every record needs a nonempty string id and values object")
        if set(record["values"]) - set(fields):
            raise ValueError("values must contain only explicitly selected compare_fields")
        if "content_hash" in record and (not isinstance(record["content_hash"], str) or not record["content_hash"]):
            raise ValueError("content_hash must be a nonempty string when present")
        canonical(record)
        indexed[record["id"]].append(record)
    age = (now - captured).total_seconds() / 3600
    return indexed, {"captured_at": data["captured_at"], "age_hours": round(age, 4),
                     "complete": data["complete"], "fresh": 0 <= age <= maximum,
                     "max_age_hours": maximum}


def receipt_index(data, now):
    if data is None:
        return {}
    if not isinstance(data, dict) or set(data) != {"schema_version", "records"} or type(data["schema_version"]) is not int or data["schema_version"] != 1 or not isinstance(data["records"], list):
        raise ValueError("Receipts require schema_version 1 and a records list")
    groups = defaultdict(list)
    for row in data["records"]:
        if not isinstance(row, dict) or set(row) != {"id", "status", "observed_at"}:
            raise ValueError("Receipt keys must be id, status, observed_at")
        if not isinstance(row["id"], str) or not row["id"].strip() or not isinstance(row["status"], str) or row["status"] not in PROTECTED | {"failed"}:
            raise ValueError("Invalid receipt identity or status")
        date = timestamp(row["observed_at"])
        groups[row["id"]].append((date, row))
    result = {}
    for identifier, entries in groups.items():
        latest = max(date for date, _ in entries)
        statuses = {row["status"] for date, row in entries if date == latest}
        result[identifier] = {
            "status": sorted(statuses), "observed_at": latest.isoformat(),
            "conflict": len(statuses) > 1 or latest > now,
            "history_protected": any(row["status"] in PROTECTED for _, row in entries),
            "evidence_count": len(entries),
        }
    return result


def reconcile(source, local, receipts=None, now=None):
    now = now or datetime.now(timezone.utc)
    sources, source_state = validate_snapshot(source, now)
    locals_, local_state = validate_snapshot(local, now)
    fields = sorted(source["compare_fields"])
    if set(fields) != set(local["compare_fields"]):
        raise ValueError("Both snapshots must select the same comparison fields")
    evidence = receipt_index(receipts, now)
    hash_ids = defaultdict(set)
    for rows in list(sources.values()) + list(locals_.values()):
        for row in rows:
            if row.get("content_hash"):
                hash_ids[row["content_hash"]].add(row["id"])
    all_ids = set(sources) | set(locals_) | set(evidence)
    records = []
    for identifier in sorted(all_ids):
        a, b = sources.get(identifier, []), locals_.get(identifier, [])
        receipt = evidence.get(identifier)
        result = {"id": identifier, "classification": "ambiguous", "changed_fields": [],
                  "reasons": [], "history_protected": bool(receipt and receipt["history_protected"])}
        if receipt:
            result["receipt"] = receipt
        reasons = result["reasons"]
        if len(a) > 1 or len(b) > 1:
            reasons.append("Repeated stable ID within a snapshot")
        if not source_state["fresh"] or not local_state["fresh"]:
            reasons.append("Stale or future-dated snapshot; refresh before planning changes")
        if receipt and receipt["conflict"]:
            reasons.append("Conflicting or future-dated receipt evidence")
        if any(set(fields) - set(row["values"]) for row in a + b):
            reasons.append("A selected comparison field is missing")
        if receipt and b and "status" in b[0]["values"]:
            status = b[0]["values"]["status"]
            if status not in receipt["status"]:
                reasons.append("Local status disagrees with latest receipt; reconcile evidence first")
        if a and not b and not local_state["complete"]:
            reasons.append("Local snapshot is incomplete; absence is not established")
        if b and not a and not source_state["complete"]:
            reasons.append("Source snapshot is incomplete; absence is not established")
        if receipt and a and not b:
            reasons.append("Receipt exists without a local record; recover history before adding")
        if reasons:
            records.append(result)
            continue
        peers = set()
        for row in a + b:
            peers.update(hash_ids.get(row.get("content_hash"), set()))
        peers.discard(identifier)
        if peers:
            result["classification"] = "duplicate"
            result["related_ids"] = sorted(peers)
            reasons.append("Matching supplied content hash across distinct IDs; review identity, do not merge automatically")
        elif a and b:
            changed = [f for f in fields if canonical(a[0]["values"][f]) != canonical(b[0]["values"][f])]
            if a[0].get("content_hash") != b[0].get("content_hash"):
                changed.append("content_hash")
            result["changed_fields"] = changed
            result["classification"] = "changed" if changed else "unchanged"
        elif a:
            result["classification"] = "new"
        elif b:
            result["classification"] = "missing-from-source"
            reasons.append("Absent in this complete snapshot, not proof of deletion")
        else:
            reasons.append("Receipt has no corresponding record in either snapshot")
        if result["history_protected"]:
            reasons.append("Preserve all scheduling/delivery evidence in any separately approved repair")
        records.append(result)
    counts = Counter(row["classification"] for row in records)
    return {"schema_version": 1, "source": source_state, "local": local_state,
            "review_required": any(counts[s] for s in STATES if s != "unchanged") or
                               not all(state["fresh"] and state["complete"] for state in (source_state, local_state)),
            "counts": {state: counts[state] for state in STATES}, "records": records,
            "mutations_performed": False,
            "next_step": "Review evidence, capture a verified backup and approve a project-specific repair separately"}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--local", required=True, type=Path)
    parser.add_argument("--receipts", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        report = reconcile(read_json(args.source), read_json(args.local),
                           read_json(args.receipts) if args.receipts else None)
        if args.json:
            print(json.dumps(report, indent=2, ensure_ascii=True))
        else:
            for row in report["records"]:
                print(f"{row['classification']}: {row['id']}")
                for reason in row["reasons"]:
                    print("  " + reason)
            print("SUMMARY: " + ", ".join(f"{k}={v}" for k, v in report["counts"].items()))
            print(report["next_step"])
        return 1 if report["review_required"] else 0
    except (ValueError, OSError) as exc:
        message = "Cannot read an input snapshot" if isinstance(exc, OSError) else str(exc)
        if args.json:
            print(json.dumps({"schema_version": 1, "error": message}))
        else:
            print("ERROR: " + message, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
