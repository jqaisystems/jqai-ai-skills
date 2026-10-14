#!/usr/bin/env python3
"""Conservative local skill-copy installer, shared by both shell entrypoints."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import uuid

RECEIPT = ".jqai-install.json"
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def check_path(path: Path) -> Path:
    """Reject linked components before resolving or reading their targets."""
    if str(path).startswith(("\\\\", "//")):
        raise ValueError("Network targets are not supported.")
    path = Path(os.path.abspath(path))
    for part in reversed((path, *path.parents)):
        try:
            info = part.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise ValueError("Linked/reparse paths are protected; inspect them manually.")
    return path


def inventory(root: Path, ignore_receipt: bool = False) -> dict[str, str]:
    check_path(root)
    result = {}
    def unreadable(_error):
        raise ValueError("Directory inventory is incomplete; installation stopped.")
    for parent, dirs, files in os.walk(root, followlinks=False, onerror=unreadable):
        for name in dirs + files:
            item = Path(parent) / name
            check_path(item)
            info = item.lstat()
            if not (stat.S_ISREG(info.st_mode) or stat.S_ISDIR(info.st_mode)):
                raise ValueError("Special filesystem entries are not supported.")
        for name in sorted(files):
            item = Path(parent) / name
            rel = item.relative_to(root).as_posix()
            if rel == RECEIPT:
                if ignore_receipt:
                    continue
                raise ValueError("Source contains a reserved installer receipt.")
            result[rel] = hashlib.sha256(item.read_bytes()).hexdigest()
    return result


def managed_files(destination: Path, skill: str) -> dict[str, str]:
    check_path(destination / RECEIPT)
    try:
        data = json.loads((destination / RECEIPT).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        raise ValueError("Existing destination is unmanaged; use a new target.") from None
    if not isinstance(data, dict) or data.get("version") != 1 or data.get("skill") != skill:
        raise ValueError("Installer receipt is not recognized.")
    current = inventory(destination, ignore_receipt=True)
    if current != data.get("files"):
        raise ValueError("Existing managed copy has local changes; preserve it and use a new target.")
    return current


def plan(root: Path, target: Path, names: list[str], replace: bool) -> list[dict]:
    root, target = check_path(root), check_path(target)
    if target == root or root in target.parents or target in root.parents:
        raise ValueError("Install target must not overlap the repository.")
    plans = []
    for name in names:
        if not NAME.fullmatch(name):
            raise ValueError("Invalid skill name.")
        source = check_path(root / "skills" / name)
        if not source.is_dir() or not (source / "SKILL.md").is_file():
            raise ValueError("Selected skill does not exist.")
        source_files = inventory(source)
        dest = check_path(target / name)
        action = "install"
        old_files = None
        if os.path.lexists(dest):
            if not dest.is_dir():
                raise ValueError("Existing destination is not a directory.")
            old_files = managed_files(dest, name)
            if old_files == source_files:
                action = "unchanged"
            elif replace:
                action = "replace-with-backup"
            else:
                raise ValueError("A managed copy exists; review changes and use --replace.")
        plans.append({"skill": name, "action": action, "files": source_files, "old_files": old_files})
    return plans


def install(root: Path, target: Path, names: list[str], replace=False, dry_run=False) -> list[dict]:
    plans = plan(root, target, names, replace)
    if dry_run:
        return plans
    target = check_path(target)
    target.mkdir(parents=True, exist_ok=True)
    for item in plans:
        name, action = item["skill"], item["action"]
        if action == "unchanged":
            continue
        source = check_path(root / "skills" / name)
        dest = check_path(target / name)
        staging = target / (".jqai-stage-" + uuid.uuid4().hex)
        staging.mkdir()
        # No recursive deletion, including on failure. Leftover staging is reviewable.
        for relative in item["files"]:
            src = check_path(source / relative)
            out = staging / relative
            out.parent.mkdir(parents=True, exist_ok=True)
            with out.open("xb") as handle:
                handle.write(src.read_bytes())
        if inventory(staging) != item["files"]:
            raise ValueError("Source changed during copying; staging was retained.")
        receipt = {"version": 1, "skill": name, "files": item["files"]}
        with (staging / RECEIPT).open("x", encoding="utf-8") as handle:
            json.dump(receipt, handle, sort_keys=True, indent=2)
            handle.write("\n")
        check_path(target)
        check_path(dest)
        backup = None
        if action == "replace-with-backup":
            if managed_files(dest, name) != item["old_files"]:
                raise ValueError("Destination changed during copying; staging was retained.")
            backup = target / ("." + name + ".backup-" + uuid.uuid4().hex)
            dest.rename(backup)
        elif os.path.lexists(dest):
            raise ValueError("Destination appeared during copying; staging was retained.")
        try:
            staging.rename(dest)
        except OSError:
            if backup is not None and not os.path.lexists(dest):
                backup.rename(dest)
            raise
    return plans


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill", nargs="?", default="web-scraper")
    parser.add_argument("--target", type=Path, default=Path.home() / ".codex" / "skills")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--replace", action="store_true")
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parents[1]
    try:
        available = sorted(p.name for p in (root / "skills").iterdir()
                           if NAME.fullmatch(p.name) and (p / "SKILL.md").is_file())
        if args.list:
            print("\n".join(available))
            return 0
        plans = install(root, args.target, available if args.all else [args.skill],
                        args.replace, args.dry_run)
        for item in plans:
            print(("PLAN " if args.dry_run else "") + item["action"] + ": " + item["skill"])
        if not args.dry_run:
            print("Retain any backup folders. Reload your tool and verify skill discovery.")
        return 0
    except ValueError as exc:
        print("STOP: " + str(exc), file=sys.stderr)
    except OSError:
        print("STOP: filesystem operation failed; inspect the private target and retained staging.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
