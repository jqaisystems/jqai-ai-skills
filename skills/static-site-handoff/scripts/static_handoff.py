#!/usr/bin/env python3
"""Package completed local static exports; never build, upload, or delete remotely."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import sys
import tempfile

VERSION = 1
HEX = re.compile(r"[0-9a-f]{64}")
RESERVED = {"con", "prn", "aux", "nul", *(f"com{i}" for i in range(1, 10)),
            *(f"lpt{i}" for i in range(1, 10))}
DENIED = {".git", ".ssh", ".npmrc", ".pypirc", "node_modules", "package.json",
          "package-lock.json", "pyproject.toml", "config.json", "config.toml",
          "credentials.json", "secrets.json", "id_rsa", "id_ed25519"}
DENIED_SUFFIXES = {".pem", ".key", ".p12", ".pfx", ".sqlite", ".sqlite3", ".db",
                   ".toml", ".yaml", ".yml", ".map"}


class HandoffError(ValueError):
    pass


def fail(message):
    raise HandoffError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def local_path(value):
    raw = str(value)
    if "://" in raw or raw.startswith(("\\\\", "//")):
        fail("Only local paths are supported.")
    path = Path(os.path.abspath(raw))
    for part in [*reversed(path.parents), path]:
        try:
            info = part.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            fail("Links and reparse points are not supported.")
    return path


def separated(*paths):
    for i, left in enumerate(paths):
        for right in paths[i + 1:]:
            if left == right or left in right.parents or right in left.parents:
                fail("Build, package, and state paths must not overlap.")


def relative_name(name):
    if not isinstance(name, str) or not name or "\\" in name or ":" in name:
        fail("Invalid relative file path.")
    parts = PurePosixPath(name).parts
    if PurePosixPath(name).is_absolute() or "/".join(parts) != name:
        fail("Non-canonical relative file path.")
    for part in parts:
        if part in {".", ".."} or part.endswith((" ", ".")) or any(ord(c) < 32 for c in part):
            fail("Unsafe relative file path.")
        if part.split(".")[0].lower() in RESERVED:
            fail("Non-portable file name.")
        lower = part.lower()
        if lower in DENIED or lower == ".env" or lower.startswith(".env."):
            fail("Credential or configuration file refused.")
    if PurePosixPath(name).suffix.lower() in DENIED_SUFFIXES:
        fail("Source, configuration, or sensitive file type refused.")
    return name


def file_hash(path):
    path = local_path(path)
    if not stat.S_ISREG(path.stat().st_mode):
        fail("Only regular files are supported.")
    total = 0
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(block)
            total += len(block)
    return {"size": total, "sha256": result.hexdigest()}


def snapshot(folder):
    folder = local_path(folder)
    if not folder.is_dir():
        fail("A required directory is missing.")
    result, seen = {}, set()
    def walk_error(_):
        fail("Directory enumeration failed.")
    for root, dirs, files in os.walk(folder, followlinks=False, onerror=walk_error):
        for name in dirs + files:
            path = local_path(Path(root) / name)
            relative = relative_name(path.relative_to(folder).as_posix())
            if relative.casefold() in seen:
                fail("Case-insensitive path collision.")
            seen.add(relative.casefold())
            if name in files:
                result[relative] = file_hash(path)
    return dict(sorted(result.items()))


def fields(value, keys):
    if not isinstance(value, dict) or set(value) != set(keys):
        fail("Invalid record fields.")


def validate_files(value):
    if not isinstance(value, dict):
        fail("Invalid file manifest.")
    seen = set()
    for name, record in value.items():
        relative_name(name)
        if name.casefold() in seen:
            fail("Case-insensitive manifest collision.")
        seen.add(name.casefold())
        fields(record, {"size", "sha256"})
        if type(record["size"]) is not int or record["size"] < 0:
            fail("Invalid file size.")
        if not isinstance(record["sha256"], str) or not HEX.fullmatch(record["sha256"]):
            fail("Invalid file hash.")


def load_json(path):
    path = local_path(path)
    if not path.is_file() or path.stat().st_size > 16 * 1024 * 1024:
        fail("Missing or oversized record.")
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                fail("Duplicate JSON field.")
            result[key] = value
        return result
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique)
    except (UnicodeError, json.JSONDecodeError):
        fail("Invalid JSON record.")


def save_json(path, value):
    path = local_path(path)
    fd, temporary = tempfile.mkstemp(prefix=".handoff-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(canonical(value) + b"\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


@contextmanager
def locked(state_dir):
    state_dir = local_path(state_dir)
    state_dir.mkdir(parents=True, exist_ok=True)
    lock = state_dir / ".handoff.lock"
    try:
        lock.mkdir()
    except FileExistsError:
        fail("State is locked; investigate interrupted work before manually clearing the lock.")
    try:
        yield
    finally:
        lock.rmdir()


def read_state(state_dir):
    path = local_path(state_dir / "state.json")
    if not path.exists():
        return {"schema_version": VERSION, "baseline": None, "pending": None, "history": []}
    state = load_json(path)
    fields(state, {"schema_version", "baseline", "pending", "history"})
    if type(state["schema_version"]) is not int or state["schema_version"] != VERSION:
        fail("Unsupported state version.")
    if state["baseline"] is not None:
        baseline = state["baseline"]
        fields(baseline, {"id", "files"})
        if not isinstance(baseline["id"], str) or not HEX.fullmatch(baseline["id"]):
            fail("Invalid baseline identity.")
        validate_files(baseline["files"])
    if state["pending"] is not None:
        fields(state["pending"], {"id", "baseline_id"})
        if not isinstance(state["pending"]["id"], str) or not HEX.fullmatch(state["pending"]["id"]):
            fail("Invalid pending identity.")
    if not isinstance(state["history"], list):
        fail("Invalid confirmation history.")
    for item in state["history"]:
        fields(item, {"package_id", "confirmed_at", "evidence"})
        if item["evidence"] != "human_acknowledgement_not_live_verification":
            fail("Invalid history evidence.")
    return state


def verify(package_dir):
    package_dir = local_path(package_dir)
    if not package_dir.is_dir():
        fail("Package directory is missing.")
    if {p.name for p in package_dir.iterdir()} != {"manifest.json", "upload"}:
        fail("Unexpected or missing package contents.")
    manifest = load_json(package_dir / "manifest.json")
    fields(manifest, {"schema_version", "created_at", "baseline_id", "snapshot",
                      "upload", "removed", "package_id"})
    if type(manifest["schema_version"]) is not int or manifest["schema_version"] != VERSION:
        fail("Unsupported package version.")
    body = {key: value for key, value in manifest.items() if key != "package_id"}
    if manifest["package_id"] != digest(body):
        fail("Package manifest identity mismatch.")
    validate_files(manifest["snapshot"])
    validate_files(manifest["upload"])
    if not manifest["snapshot"]:
        fail("An empty export is not a complete build.")
    for name, record in manifest["upload"].items():
        if manifest["snapshot"].get(name) != record:
            fail("Upload manifest is inconsistent with the build snapshot.")
    if not isinstance(manifest["removed"], list) or len(set(manifest["removed"])) != len(manifest["removed"]):
        fail("Invalid removed-path report.")
    for name in manifest["removed"]:
        relative_name(name)
        if name in manifest["snapshot"]:
            fail("Removed path is still in the build.")
    if snapshot(package_dir / "upload") != manifest["upload"]:
        fail("Upload package files are missing, added, or modified.")
    return manifest


def prepare(build_dir, package_dir, state_dir):
    build_dir, package_dir, state_dir = map(local_path, (build_dir, package_dir, state_dir))
    separated(build_dir, package_dir, state_dir)
    if package_dir.exists():
        fail("Package output already exists.")
    if not package_dir.parent.is_dir():
        fail("Package parent must already exist.")
    with locked(state_dir):
        state = read_state(state_dir)
        baseline = state["baseline"]
        files = snapshot(build_dir)
        if not files:
            fail("An empty export is not a complete build.")
        old = baseline["files"] if baseline else {}
        changed = {name: record for name, record in files.items() if old.get(name) != record}
        body = {"schema_version": VERSION, "created_at": timestamp(),
                "baseline_id": baseline["id"] if baseline else None,
                "snapshot": files, "upload": changed, "removed": sorted(set(old) - set(files))}
        manifest = {**body, "package_id": digest(body)}
        with tempfile.TemporaryDirectory(prefix=".handoff-", dir=package_dir.parent) as temporary:
            stage = Path(temporary) / "package"
            (stage / "upload").mkdir(parents=True)
            for name in changed:
                target = stage / "upload" / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(local_path(build_dir / name), target)
            save_json(stage / "manifest.json", manifest)
            verify(stage)
            if snapshot(build_dir) != files:
                fail("Build changed while preparing the package.")
            if package_dir.exists():
                fail("Package destination appeared during preparation.")
            stage.rename(package_dir)
        # A crash before this atomic update leaves an unregistered package, never a new baseline.
        state["pending"] = {"id": manifest["package_id"], "baseline_id": manifest["baseline_id"]}
        save_json(state_dir / "state.json", state)
    return manifest


def confirm(package_dir, state_dir, package_id, acknowledge_upload=False):
    package_dir, state_dir = map(local_path, (package_dir, state_dir))
    separated(package_dir, state_dir)
    if not acknowledge_upload:
        fail("Confirmation requires an explicit upload acknowledgement.")
    with locked(state_dir):
        state = read_state(state_dir)
        manifest = verify(package_dir)
        baseline_id = state["baseline"]["id"] if state["baseline"] else None
        expected = {"id": package_id, "baseline_id": baseline_id}
        if manifest["package_id"] != package_id or manifest["baseline_id"] != baseline_id or state["pending"] != expected:
            fail("Stale, altered, or unregistered package confirmation.")
        old = state["baseline"]["files"] if state["baseline"] else {}
        expected_upload = {name: value for name, value in manifest["snapshot"].items()
                           if old.get(name) != value}
        if expected_upload != manifest["upload"] or sorted(set(old) - set(manifest["snapshot"])) != manifest["removed"]:
            fail("Package is inconsistent with the confirmed baseline.")
        state["baseline"] = {"id": package_id, "files": manifest["snapshot"]}
        state["pending"] = None
        state["history"].append({"package_id": package_id, "confirmed_at": timestamp(),
                                "evidence": "human_acknowledgement_not_live_verification"})
        save_json(state_dir / "state.json", state)
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("prepare", "verify", "confirm"):
        command = commands.add_parser(name)
        command.add_argument("--package-dir", required=True, type=Path)
        command.add_argument("--json", action="store_true")
        if name != "verify":
            command.add_argument("--state-dir", required=True, type=Path)
        if name == "prepare":
            command.add_argument("--build-dir", required=True, type=Path)
        if name == "confirm":
            command.add_argument("--package-id", required=True)
            command.add_argument("--acknowledge-upload", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "prepare":
            result = prepare(args.build_dir, args.package_dir, args.state_dir)
        elif args.command == "verify":
            result = verify(args.package_dir)
        else:
            result = confirm(args.package_dir, args.state_dir, args.package_id, args.acknowledge_upload)
        report = {"status": "PASS", "operation": args.command, "package_id": result["package_id"],
                  "upload_files": len(result["upload"]), "removed_paths": result["removed"],
                  "live_deployment": "unverified"}
        code = 0
    except HandoffError as exc:
        report = {"status": "FAIL", "reason": str(exc)}
        code = 1
    except (OSError, ValueError, TypeError):
        report = {"status": "FAIL", "reason": "Operation refused; check local inputs, package integrity, state and locks."}
        code = 1
    print(json.dumps(report, indent=2) if args.json else "\n".join(f"{k}: {v}" for k, v in report.items()))
    return code


if __name__ == "__main__":
    sys.exit(main())

