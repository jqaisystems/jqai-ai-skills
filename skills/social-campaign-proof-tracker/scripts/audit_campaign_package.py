#!/usr/bin/env python3
"""Read-only campaign fingerprint and evidence audit. Never publish or authorize a send."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys

HEX = re.compile(r"[0-9a-f]{64}")
MEDIA = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".avif", ".mp4", ".mov", ".webm", ".pdf"}
STATES = {"scheduled", "published", "verified", "failed", "uncertain"}


class AuditError(ValueError):
    pass


def require(condition, message="Invalid evidence contract."):
    if not condition:
        raise AuditError(message)


def fields(value, expected):
    require(isinstance(value, dict) and set(value) == set(expected))


def text_value(value, empty=False):
    require(isinstance(value, str) and (empty or bool(value.strip())))
    return value


def date(value):
    text_value(value)
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise AuditError("A timestamp is invalid.") from None
    require(result.tzinfo is not None and result.utcoffset() is not None, "Timestamps need an explicit offset.")
    return result


def local_path(value):
    raw = str(value)
    require("://" not in raw and not raw.startswith(("\\\\", "//")), "Local files only.")
    path = Path(os.path.abspath(raw))
    for part in [*reversed(path.parents), path]:
        try:
            info = part.lstat()
        except FileNotFoundError:
            continue
        require(not stat.S_ISLNK(info.st_mode) and not getattr(info, "st_file_attributes", 0) & 0x400,
                "Links and reparse points are unsupported.")
    return path


def read_json(path):
    path = local_path(path)
    require(path.is_file() and path.stat().st_size <= 1024 * 1024, "Missing or oversized evidence file.")
    def unique(pairs):
        output = {}
        for key, value in pairs:
            require(key not in output, "Duplicate JSON field.")
            output[key] = value
        return output
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique)
    except (UnicodeError, json.JSONDecodeError):
        raise AuditError("Invalid JSON evidence.") from None


def hash_media(root, name):
    text_value(name)
    parts = PurePosixPath(name).parts
    require(parts and not PurePosixPath(name).is_absolute() and "\\" not in name and ":" not in name
            and "/".join(parts) == name and all(p not in {".", ".."} for p in parts), "Unsafe media path.")
    path = local_path(root / name)
    require(root in path.parents and path.suffix.lower() in MEDIA, "Unsupported media input.")
    require(stat.S_ISREG(path.stat().st_mode), "Media must be a regular file.")
    value, size = hashlib.sha256(), 0
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
            size += len(block)
    return {"sha256": value.hexdigest(), "size": size}


def package_fingerprint(package, root):
    fields(package, {"schema_version", "provider", "destination", "scheduled_at", "posts"})
    require(type(package["schema_version"]) is int and package["schema_version"] == 1)
    text_value(package["provider"])
    text_value(package["destination"])
    if package["scheduled_at"] is not None:
        date(package["scheduled_at"])
    require(isinstance(package["posts"], list) and 0 < len(package["posts"]) <= 100)
    frozen = {**package, "posts": []}
    for post in package["posts"]:
        fields(post, {"copy", "title", "media"})
        text_value(post["copy"], empty=True)
        text_value(post["title"], empty=True)
        require(isinstance(post["media"], list) and len(post["media"]) <= 100)
        media = []
        for item in post["media"]:
            fields(item, {"path", "role", "alt_text"})
            text_value(item["role"])
            text_value(item["alt_text"], empty=True)
            media.append({**item, **hash_media(root, item["path"])})
        require(post["copy"] or post["title"] or media, "Empty publication item.")
        frozen["posts"].append({**post, "media": media})
    encoded = json.dumps(frozen, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def audit(package_path, approval_path=None, receipts_path=None, now=None):
    now = now or datetime.now(timezone.utc)
    require(now.tzinfo is not None)
    package_path = local_path(package_path)
    package = read_json(package_path)
    fingerprint = package_fingerprint(package, package_path.parent)
    findings, approval_matches = [], False
    if approval_path is not None:
        approval = read_json(approval_path)
        fields(approval, {"schema_version", "fingerprint", "decision", "approved_at"})
        require(type(approval["schema_version"]) is int and approval["schema_version"] == 1)
        require(approval["decision"] in {"approved", "rejected"})
        require(isinstance(approval["fingerprint"], str) and HEX.fullmatch(approval["fingerprint"]))
        approval_matches = (approval["decision"] == "approved"
                            and approval["fingerprint"] == fingerprint
                            and date(approval["approved_at"]) <= now)
        if not approval_matches:
            findings.append("approval_record_does_not_match")
    else:
        findings.append("approval_record_missing")
    state = "approved" if approval_matches else "prepared"
    matching = []
    records = []
    if receipts_path is not None:
        pack = read_json(receipts_path)
        fields(pack, {"schema_version", "records"})
        require(type(pack["schema_version"]) is int and pack["schema_version"] == 1
                and isinstance(pack["records"], list) and len(pack["records"]) <= 1000)
        records = pack["records"]
        for record in records:
            fields(record, {"provider", "destination", "fingerprint", "state",
                            "observed_at", "receipt_id"})
            for key in ("provider", "destination", "receipt_id"):
                text_value(record[key])
            require(isinstance(record["fingerprint"], str) and HEX.fullmatch(record["fingerprint"]))
            require(record["state"] in STATES)
            observed = date(record["observed_at"])
            if observed > now:
                findings.append("future_dated_receipt")
            if any(record[key] != package[key] for key in ("provider", "destination")):
                findings.append("receipt_identity_conflict")
            elif record["fingerprint"] != fingerprint:
                findings.append("receipt_package_conflict")
            elif observed <= now:
                matching.append(record)
        if not records:
            findings.append("empty_receipts_are_not_cancellation_evidence")
    if matching:
        ids = {r["receipt_id"] for r in matching}
        states = {r["state"] for r in matching}
        serialized = [json.dumps(r, sort_keys=True) for r in matching]
        if len(ids) != 1:
            findings.append("multiple_delivery_identities")
        if len(set(serialized)) != len(serialized):
            findings.append("duplicate_receipt_evidence")
        if "uncertain" in states or ("failed" in states and len(states) > 1):
            findings.append("conflicting_or_uncertain_receipts")
        ordered = sorted(matching, key=lambda r: date(r["observed_at"]))
        rank = {"scheduled": 1, "published": 2, "verified": 3}
        for previous, current in zip(ordered, ordered[1:]):
            if (date(previous["observed_at"]) == date(current["observed_at"])
                    and previous["state"] != current["state"]):
                findings.append("conflicting_or_uncertain_receipts")
            elif (previous["state"] in rank and current["state"] in rank
                  and rank[current["state"]] < rank[previous["state"]]):
                findings.append("receipt_state_regression")
        state = ordered[-1]["state"]
        if state == "verified":
            findings.append("verification_is_supplied_evidence_not_a_live_check")
    conflicts = {"future_dated_receipt", "receipt_identity_conflict", "receipt_package_conflict",
                 "multiple_delivery_identities", "duplicate_receipt_evidence",
                 "conflicting_or_uncertain_receipts", "receipt_state_regression"}
    if conflicts.intersection(findings):
        state = "uncertain"
    if package["scheduled_at"] is not None and date(package["scheduled_at"]) <= now and not matching:
        findings.append("past_schedule_requires_review_not_post_now")
    if any(not item["alt_text"] for post in package["posts"] for item in post["media"]):
        findings.append("empty_alt_text_requires_review")
    return {"schema_version": 1, "fingerprint": fingerprint, "state": state,
            "approval_record_matches": approval_matches, "human_consent_authenticated": False,
            "receipt_count": len(records), "matching_receipt_count": len(matching),
            "findings": sorted(set(findings)), "live_state_verified": False,
            "retry": "reconcile_before_any_retry", "external_action_authorized": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", required=True, type=Path)
    parser.add_argument("--approval", type=Path)
    parser.add_argument("--receipts", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        result = audit(args.package, args.approval, args.receipts)
        code = 0 if result["approval_record_matches"] and result["state"] != "uncertain" and not (
            set(result["findings"]) - {"verification_is_supplied_evidence_not_a_live_check"}) else 2
    except AuditError as exc:
        result = {"status": "ERROR", "reason": str(exc), "external_action_authorized": False}
        code = 1
    except (OSError, ValueError, TypeError):
        result = {"status": "ERROR", "reason": "Evidence could not be audited; no action authorized."}
        code = 1
    print(json.dumps(result, indent=2) if args.json else "\n".join(f"{k}: {v}" for k, v in result.items()))
    return code


if __name__ == "__main__":
    sys.exit(main())

