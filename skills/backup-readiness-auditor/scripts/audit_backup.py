#!/usr/bin/env python3
"""Evaluate supplied evidence only. Never inspect or operate on a backup."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import stat
import sys

ID = re.compile(r"[a-z0-9][a-z0-9-]{0,63}")
COUNTS = ("expected_files", "verified_files", "hash_mismatches", "read_errors",
          "cloud_only_files", "unresolved_links")


def timestamp(value):
    if not isinstance(value, str):
        raise ValueError("Invalid timestamp.")
    try:
        date = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise ValueError("Invalid timestamp.") from None
    if date.tzinfo is None:
        raise ValueError("Timestamp needs an explicit timezone.")
    return date.astimezone(timezone.utc)


def fields(obj, keys):
    if not isinstance(obj, dict) or set(obj) != set(keys):
        raise ValueError("Missing or unsupported fields.")


def number(value):
    if type(value) is not int or value < 0:
        raise ValueError("Counts must be nonnegative integers.")


def boolean(value):
    if value is not None and type(value) is not bool:
        raise ValueError("Expected true, false, or null.")


def audit(data, as_of, max_age_days=7):
    if not isinstance(as_of, datetime) or as_of.tzinfo is None:
        raise ValueError("Evidence cutoff needs a timezone.")
    if type(max_age_days) is not int or max_age_days < 0:
        raise ValueError("Freshness window must be nonnegative.")
    fields(data, ("version", "scope_complete", "required_ids", "destination", "records"))
    if type(data["version"]) is not int or data["version"] != 1:
        raise ValueError("Unsupported evidence version.")
    boolean(data["scope_complete"])
    required = data["required_ids"]
    if not isinstance(required, list) or not required or any(not isinstance(x, str) or not ID.fullmatch(x) for x in required):
        raise ValueError("Invalid required dataset IDs.")
    if len(required) != len(set(required)):
        raise ValueError("Duplicate required dataset IDs.")
    dest = data["destination"]
    fields(dest, ("independent", "free_bytes", "remaining_bytes", "reserve_bytes"))
    boolean(dest["independent"])
    for key in ("free_bytes", "remaining_bytes", "reserve_bytes"):
        number(dest[key])
    reasons = []
    def add(level, code, dataset=None):
        reasons.append({"level": level, "code": code, "dataset": dataset})
    if data["scope_complete"] is not True:
        add("review", "scope-unconfirmed")
    if dest["independent"] is False:
        add("block", "destination-not-independent")
    elif dest["independent"] is None:
        add("review", "destination-independence-unknown")
    if dest["free_bytes"] < dest["remaining_bytes"] + dest["reserve_bytes"]:
        add("block", "insufficient-remaining-capacity")
    if not isinstance(data["records"], list):
        raise ValueError("Records must be a list.")
    seen = set()
    for row in data["records"]:
        fields(row, ("id", "captured_at", *COUNTS, "snapshot_consistent", "restore_test"))
        name = row["id"]
        if not isinstance(name, str) or not ID.fullmatch(name) or name in seen:
            raise ValueError("Invalid or duplicate dataset ID.")
        seen.add(name)
        captured = timestamp(row["captured_at"])
        age = (as_of - captured).total_seconds()
        if age < 0:
            add("review", "future-evidence", name)
        elif age > max_age_days * 86400:
            add("review", "stale-evidence", name)
        for key in COUNTS:
            number(row[key])
        if row["verified_files"] > row["expected_files"]:
            raise ValueError("Verified count exceeds expected count.")
        if row["verified_files"] < row["expected_files"]:
            add("block", "incomplete-file-verification", name)
        for key in COUNTS[2:]:
            if row[key]:
                add("block", key.replace("_", "-"), name)
        boolean(row["snapshot_consistent"])
        if row["snapshot_consistent"] is False:
            add("block", "inconsistent-snapshot", name)
        elif row["snapshot_consistent"] is None:
            add("review", "snapshot-consistency-unknown", name)
        if row["restore_test"] not in ("passed", "failed", "not_run"):
            raise ValueError("Invalid restore-test status.")
        if row["restore_test"] == "failed":
            add("block", "restore-test-failed", name)
        elif row["restore_test"] == "not_run":
            add("review", "restore-test-not-run", name)
    for missing in sorted(set(required) - seen):
        add("block", "missing-required-dataset", missing)
    verdict = "BLOCKED" if any(r["level"] == "block" for r in reasons) else "REVIEW" if reasons else "EVIDENCE_COMPLETE"
    return {"version": 1, "verdict": verdict, "as_of": as_of.isoformat(),
            "max_age_days": max_age_days, "record_count": len(seen), "reasons": reasons,
            "independently_verified": False, "destructive_action_authorized": False}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key.")
        result[key] = value
    return result


def load_pack(path):
    if str(path).startswith(("\\\\", "//")):
        raise ValueError("Network input is not supported.")
    path = Path(os.path.abspath(path))
    for part in (path, *path.parents):
        info = part.lstat()
        flags = getattr(info, "st_file_attributes", 0)
        if stat.S_ISLNK(info.st_mode) or flags & (0x400 | 0x1000 | 0x40000 | 0x400000):
            raise ValueError("Linked or offline input is not supported.")
    if not path.is_file():
        raise ValueError("Input must be an ordinary file.")
    with path.open("rb") as handle:
        raw = handle.read(1048577)
    if len(raw) > 1048576:
        raise ValueError("Evidence pack exceeds 1 MiB.")
    try:
        return json.loads(raw.decode("utf-8-sig"), object_pairs_hook=unique_object)
    except (UnicodeError, json.JSONDecodeError):
        raise ValueError("Invalid evidence JSON; source text withheld.") from None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--as-of", required=True)
    parser.add_argument("--max-age-days", type=int, default=7)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = audit(load_pack(args.input), timestamp(args.as_of), args.max_age_days)
    except (OSError, ValueError, TypeError, OverflowError, RecursionError):
        error = {"error": "Invalid or unreadable evidence pack; content and location withheld."}
        print(json.dumps(error) if args.json else error["error"], file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(result["verdict"] + ": supplied evidence only, not independently verified.")
        for reason in result["reasons"]:
            print(reason["level"] + ": " + reason["code"] + (" [" + reason["dataset"] + "]" if reason["dataset"] else ""))
        print("No destructive action is authorized.")
    return 0 if result["verdict"] == "EVIDENCE_COMPLETE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
