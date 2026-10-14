#!/usr/bin/env python3
"""Build private reinstall reports from a metadata-only software inventory."""
from __future__ import annotations
import argparse
import csv
from datetime import datetime
import hashlib
import io
import json
from pathlib import Path
import sys

SOURCES = {"registry-machine", "registry-machine-32", "registry-user", "store-current-user", "start-menu"}
FIELDS = {"record_id", "source", "name", "version", "publisher", "package_id", "evidence"}
OUTPUTS = ("software-inventory.csv", "reinstall-checklist.md", "coverage-report.md")


def validate(data):
    if not isinstance(data, dict) or set(data) != {"schema_version", "captured_at", "coverage", "records"} or type(data["schema_version"]) is not int or data["schema_version"] != 1:
        raise ValueError("Inventory must match schema_version 1")
    if not isinstance(data["captured_at"], str):
        raise ValueError("captured_at must be a timezone-aware ISO timestamp")
    date = datetime.fromisoformat(data["captured_at"].replace("Z", "+00:00"))
    if date.tzinfo is None:
        raise ValueError("captured_at requires a timezone")
    if not isinstance(data["records"], list) or not isinstance(data["coverage"], list):
        raise ValueError("records and coverage must be lists")
    ids = set()
    for row in data["records"]:
        if not isinstance(row, dict) or set(row) != FIELDS or any(not isinstance(v, str) for v in row.values()):
            raise ValueError("Invalid software record")
        if not row["record_id"] or row["record_id"] in ids or not row["name"].strip():
            raise ValueError("Record IDs must be unique and names must be nonempty")
        if row["source"] not in SOURCES or row["evidence"] not in {"registered", "shortcut-only"}:
            raise ValueError("Unknown evidence source or type")
        if (row["source"] == "start-menu") != (row["evidence"] == "shortcut-only"):
            raise ValueError("Evidence type does not match its source")
        ids.add(row["record_id"])
    seen = set()
    for item in data["coverage"]:
        if not isinstance(item, dict) or set(item) != {"source", "status", "count"}:
            raise ValueError("Invalid coverage entry")
        if not isinstance(item["source"], str) or item["source"] not in {"Registry", "Store", "StartMenu"} or item["source"] in seen:
            raise ValueError("Coverage sources must be unique known adapters")
        if not isinstance(item["status"], str) or item["status"] not in {"complete", "unavailable"} or type(item["count"]) is not int or item["count"] < 0:
            raise ValueError("Invalid coverage status or count")
        expected = sum(1 for row in data["records"] if
                       (item["source"] == "Registry" and row["source"].startswith("registry-")) or
                       (item["source"] == "Store" and row["source"] == "store-current-user") or
                       (item["source"] == "StartMenu" and row["source"] == "start-menu"))
        if expected != item["count"]:
            raise ValueError("Coverage count does not match source records")
        seen.add(item["source"])
    if seen != {"Registry", "Store", "StartMenu"}:
        raise ValueError("Coverage must account for all three adapters")
    return data


def cell(value):
    value = str(value)
    if value.lstrip().startswith(("=", "+", "-", "@")) or value.startswith(("\t", "\r", "\n")):
        return "'" + value
    return value


def md(value):
    text = str(value).replace("\r", " ").replace("\n", " ")
    for char in ("\\", chr(96), "*", "_", "[", "]", "<", ">", "|"):
        text = text.replace(char, "\\" + char)
    return text


def groups(records):
    grouped = {}
    for row in records:
        # Names alone are insufficient to merge different publishers.
        if row["package_id"].strip():
            key = ("package", row["package_id"].casefold())
        elif row["publisher"].strip():
            key = ("name-publisher", row["name"].strip().casefold(), row["publisher"].strip().casefold())
        else:
            key = ("unconfirmed", row["record_id"])
        grouped.setdefault(key, []).append(row)
    return sorted(grouped.values(), key=lambda rows: (rows[0]["name"].casefold(), rows[0]["publisher"].casefold()))


def render(data):
    data = validate(data)
    csv_buffer = io.StringIO(newline="")
    writer = csv.writer(csv_buffer, lineterminator="\n")
    columns = ["record_id", "source", "name", "version", "publisher", "package_id", "evidence",
               "reinstall_choice", "completion_status"]
    writer.writerow(columns)
    for row in data["records"]:
        writer.writerow([cell(row.get(k, "Undecided" if k == "reinstall_choice" else "Not started")) for k in columns])
    checklist = [
        "# Reinstall Checklist", "", "Private working document. Review before sharing.", "",
        "Registrations and shortcuts are evidence, not proof that software runs.",
        "Nothing is selected for reinstall automatically. CSV choices and these checkboxes do not synchronize.", "",
    ]
    for rows in groups(data["records"]):
        names = sorted({r["name"] for r in rows})
        versions = sorted({r["version"] for r in rows if r["version"]})
        evidence = "Registered, runtime unverified" if any(r["evidence"] == "registered" for r in rows) else "Shortcut only, unconfirmed"
        checklist.append(f"- [ ] {md(' / '.join(names))} | {md(', '.join(versions) or 'Version unknown')} | {evidence}")
        checklist.append("  - Evidence records: " + ", ".join(md(r["record_id"]) for r in rows))
    checklist += ["", "## Before reinstalling", "",
                  "- Review each choice and independently verify official download sources.",
                  "- Verify separate backups of needed files and settings before any destructive maintenance.",
                  "- This inventory is not a backup, an activation record, or permission to erase a drive.", ""]
    coverage = ["# Collection Coverage", "", f"Captured: {md(data['captured_at'])}", "",
                f"Evidence records: {len(data['records'])}",
                f"Conservative display groups: {len(groups(data['records']))}", "",
                "Neither count is a verified count of runnable applications.", ""]
    for source in data["coverage"]:
        coverage.append(f"- {source['source']}: {source['status']}, {source['count']} records")
    coverage += ["", "## Limits", "",
                 "Other users, portable applications, package-manager environments, browser extensions, "
                 "drivers, and remote environments are not comprehensively inventoried.",
                 "Unknown versions stay blank. Different publishers and uncertain aliases are not silently merged.",
                 "No download, installation, or software removal was performed.", ""]
    return dict(zip(OUTPUTS, (csv_buffer.getvalue(), "\n".join(checklist), "\n".join(coverage))))


def write_reports(data, output):
    output = output.expanduser().absolute()
    if str(output).startswith(("\\\\", "//")):
        raise ValueError("Choose a local private output directory")
    for ancestor in (output, *output.parents):
        if ancestor.is_symlink() or (ancestor.exists() and getattr(ancestor.stat(), "st_file_attributes", 0) & 0x400):
            raise ValueError("Linked output directories are not supported")
    rendered = render(data)
    if any((output / name).exists() for name in OUTPUTS):
        raise ValueError("A report already exists; choose a new output directory")
    output.mkdir(parents=True, exist_ok=True)
    for name, content in rendered.items():
        with (output / name).open("x", encoding="utf-8", newline="") as stream:
            stream.write(content)
    return [{"file": name, "sha256": hashlib.sha256((output / name).read_bytes()).hexdigest()} for name in OUTPUTS]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        if str(args.input).startswith(("\\\\", "//")):
            raise ValueError("Inventory must be a local file")
        source = args.input.expanduser().absolute()
        for item in (source, *source.parents):
            if item.is_symlink() or (item.exists() and getattr(item.lstat(), "st_file_attributes", 0) & 0x400):
                raise ValueError("Linked inventory paths are not supported")
        data = json.loads(source.read_text(encoding="utf-8-sig"))
        result = write_reports(data, args.output_dir)
        print(json.dumps({"reports": result, "software_changed": False}, indent=2))
        return 0
    except (OSError, ValueError) as exc:
        message = "Cannot read input or create new reports" if isinstance(exc, OSError) else str(exc)
        print("ERROR: " + message, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
