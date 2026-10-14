#!/usr/bin/env python3
"""Scan a public-release candidate for common safety risks."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
from dataclasses import dataclass, field
from pathlib import Path


SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "dist",
    "build",
    "coverage",
    "__pycache__",
    ".venv",
    "venv",
    ".next",
    ".cache",
}

BASELINE_FILENAME = ".public-safety-baseline.json"

RISKY_EXTENSIONS = {
    ".7z",
    ".csv",
    ".db",
    ".env",
    ".gz",
    ".key",
    ".kdbx",
    ".log",
    ".p12",
    ".pem",
    ".pfx",
    ".sqlite",
    ".sqlite3",
    ".tar",
    ".tsv",
    ".xls",
    ".xlsx",
    ".zip",
}

RISKY_FILENAMES = {
    ".env",
    ".env.local",
    ".env.production",
    "credentials.json",
    "secrets.json",
    "cookies.txt",
    "id_rsa",
    "id_rsa.pub",
}

CONTENT_PATTERNS: list[tuple[str, re.Pattern[str], str]] = [
    ("private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "block"),
    ("token-like secret", re.compile(r"\b(?:sk-[A-Za-z0-9_\-]{16,}|ghp_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|xox[bp]-[A-Za-z0-9\-]{20,}|AIza[A-Za-z0-9_\-]{20,})\b"), "block"),
    ("jwt-like token", re.compile(r"\beyJ[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{10,}\b"), "block"),
    ("credential keyword", re.compile(r"(?i)\b(api[_-]?key|secret|password|passwd|token|bearer|cookie|smtp|private[_-]?key)\b"), "review"),
    ("local user path", re.compile(r"(?i)(?:[A-Z]:[\\/](?:Users|Documents and Settings)[\\/]|/(?:Users|home)/[^/\s]+/)"), "review"),
    ("private wording", re.compile(r"(?i)\b(confidential|internal only|do not share|nda|invoice|client data|prospect list)\b"), "review"),
]


@dataclass
class Finding:
    severity: str
    path: str
    line: int | None
    kind: str
    detail: str
    _fingerprint: str = field(default="", repr=False)


def normalized_path(path: str) -> str:
    return path.replace("\\", "/")


def finding_fingerprint(finding: Finding) -> str:
    if finding._fingerprint:
        return finding._fingerprint
    payload = {
        "severity": finding.severity,
        "path": normalized_path(finding.path),
        "kind": finding.kind,
        "detail": finding.detail,
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def is_probably_binary(path: Path) -> bool:
    try:
        with path.open("rb") as handle:
            chunk = handle.read(4096)
    except OSError:
        return False
    return b"\0" in chunk


def is_link(path: Path) -> bool:
    info = path.lstat()
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & 0x400)


def check_baseline_path(path: Path) -> None:
    for component in (Path(os.path.abspath(path)), *Path(os.path.abspath(path)).parents):
        if os.path.lexists(component) and is_link(component):
            raise OSError("Linked baseline path")


def iter_files(root: Path):
    if not root.is_dir() or is_link(root):
        yield root
        return
    def failed(_error):
        raise OSError("Enumeration failed")
    for parent, dirs, files in os.walk(root, followlinks=False, onerror=failed):
        for name in list(dirs):
            path = Path(parent) / name
            if name in SKIP_DIRS:
                dirs.remove(name)
            elif is_link(path):
                dirs.remove(name)
                yield path
        for name in files:
            yield Path(parent) / name


def relative(path: Path, root: Path) -> str:
    if path == root:
        return "<input>"
    try:
        return str(path.relative_to(root))
    except ValueError:
        return "<outside-scope>"


def safe_location(value: str) -> str:
    for _, pattern, severity in CONTENT_PATTERNS:
        if severity == "block":
            value = pattern.sub("[redacted]", value)
    return "".join(char if char.isprintable() else "?" for char in value)


def public_finding(finding: Finding) -> dict:
    return {"severity": finding.severity, "path": safe_location(finding.path),
            "line": finding.line, "kind": finding.kind, "detail": finding.detail}


def scan_file(path: Path, root: Path) -> list[Finding]:
    findings: list[Finding] = []
    rel = relative(path, root)
    lower_name = path.name.lower()
    suffixes = {suffix.lower() for suffix in path.suffixes}
    if is_link(path):
        return [Finding("block", rel, None, "linked input", "Target was not read.")]
    if not stat.S_ISREG(path.lstat().st_mode):
        return [Finding("block", rel, None, "unsupported input", "Input was not read.")]

    if lower_name in RISKY_FILENAMES:
        findings.append(Finding("block", rel, None, "risky filename", "Restricted file name."))

    risky_suffixes = sorted(suffixes & RISKY_EXTENSIONS)
    for suffix in risky_suffixes:
        findings.append(Finding("review", rel, None, "risky extension", suffix))

    if is_probably_binary(path):
        findings.append(Finding("review", rel, None, "binary file", "binary-like content should be intentional"))
        return findings

    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            findings.append(Finding("block", rel, None, "read error", "Content could not be checked."))
            return findings
    except OSError:
        findings.append(Finding("block", rel, None, "read error", "Content could not be checked."))
        return findings

    for line_number, line in enumerate(text.splitlines(), start=1):
        for label, pattern, severity in CONTENT_PATTERNS:
            if pattern.search(line):
                snippet = line.strip()
                if len(snippet) > 140:
                    snippet = snippet[:137] + "..."
                legacy = Finding(severity, rel, line_number, label, snippet)
                findings.append(Finding(severity, rel, line_number, label,
                                        "Matched content withheld.",
                                        finding_fingerprint(legacy)))

    return findings


def scan(root: Path) -> list[Finding]:
    root = Path(os.path.abspath(root))
    for component in (root, *root.parents):
        if is_link(component):
            return [Finding("block", "<input>", None, "linked input", "Target was not read.")]
    return [finding for path in iter_files(root) for finding in scan_file(path, root)]


def default_baseline_path(target: Path) -> Path | None:
    if target.is_dir():
        return target / BASELINE_FILENAME
    return None


def load_baseline(path: Path | None) -> set[str]:
    if path is None:
        return set()
    check_baseline_path(path)
    if not path.exists():
        return set()
    try:
        if not stat.S_ISREG(path.stat().st_mode) or path.stat().st_size > 2097152:
            raise OSError("Unsupported baseline input")
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError, RecursionError):
        raise SystemExit("Could not read the baseline; its content and location are withheld.") from None
    if not isinstance(data, dict) or not isinstance(data.get("findings", []), list):
        raise SystemExit("Invalid baseline structure.")
    findings = data.get("findings", [])
    return {entry["hash"] for entry in findings if isinstance(entry, dict)
            and entry.get("severity") == "review" and isinstance(entry.get("hash"), str)}


def apply_baseline(findings: list[Finding], baseline_hashes: set[str]) -> tuple[list[Finding], int]:
    active: list[Finding] = []
    suppressed = 0
    for finding in findings:
        if finding.severity == "review" and finding_fingerprint(finding) in baseline_hashes:
            suppressed += 1
        else:
            active.append(finding)
    return active, suppressed


def write_baseline(path: Path, findings: list[Finding]) -> None:
    block_count = sum(1 for finding in findings if finding.severity == "block")
    if block_count:
        raise SystemExit(f"Refusing to baseline {block_count} blocking finding(s). Remove real risks first.")

    entries = [
        {
            "hash": finding_fingerprint(finding),
            "severity": finding.severity,
            "path": safe_location(normalized_path(finding.path)),
            "kind": finding.kind,
            "reason": "Known intentional finding for this public repo.",
        }
        for finding in sorted(findings, key=lambda item: (normalized_path(item.path), item.kind, item.detail))
    ]
    data = {
        "version": 1,
        "generated_by": "scan_public_safety.py",
        "notes": "Hashes suppress known review findings only. Blocking findings are not baselined.",
        "findings": entries,
    }
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def print_text(findings: list[Finding], target: Path, suppressed: int = 0, baseline_path: Path | None = None) -> None:
    print("Public safety scan (locations are relative; reports remain private).")
    if not findings:
        print("READY: no unbaselined common safety risks found.")
        if suppressed:
            print(f"Baseline: suppressed {suppressed} known review finding(s).")
        return

    block_count = sum(1 for finding in findings if finding.severity == "block")
    review_count = sum(1 for finding in findings if finding.severity == "review")
    verdict = "BLOCK" if block_count else "REVIEW"
    print(f"{verdict}: {block_count} blocking finding(s), {review_count} review finding(s).")
    if suppressed:
        print(f"Baseline: suppressed {suppressed} known review finding(s).")

    for finding in findings:
        location = safe_location(finding.path) if finding.line is None else f"{safe_location(finding.path)}:{finding.line}"
        detail = finding.detail.encode("ascii", errors="backslashreplace").decode("ascii")
        print(f"- [{finding.severity}] {location} - {finding.kind}: {detail}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scan a public GitHub release candidate for safety risks.")
    parser.add_argument("target", help="File or folder to scan")
    parser.add_argument("--json", action="store_true", help="Print structured JSON findings")
    parser.add_argument("--baseline", help=f"Baseline file to suppress known findings. Defaults to {BASELINE_FILENAME} in folder targets.")
    parser.add_argument("--no-baseline", action="store_true", help="Ignore any baseline file and show all findings")
    parser.add_argument("--write-baseline", action="store_true", help="Write a baseline for current non-blocking findings")
    args = parser.parse_args(argv)

    target = Path(args.target)
    if not target.exists():
        print("Target is unavailable; location withheld.", file=sys.stderr)
        return 2

    try:
        findings = scan(target)
    except OSError:
        print("Scan incomplete: a filesystem operation failed; details withheld.", file=sys.stderr)
        return 2
    protected_root = any(f.kind == "linked input" and f.path == "<input>" for f in findings)
    baseline_path = None if protected_root else (Path(args.baseline) if args.baseline else default_baseline_path(target))

    if args.write_baseline:
        if baseline_path is None:
            print("A baseline path is required when scanning a single file.", file=sys.stderr)
            return 2
        try:
            check_baseline_path(baseline_path)
            write_baseline(baseline_path, findings)
        except OSError:
            print("Baseline write failed; details withheld.", file=sys.stderr)
            return 2
        print(f"Wrote baseline with {len(findings)} review finding(s).")
        return 0

    try:
        baseline_hashes = set() if args.no_baseline else load_baseline(baseline_path)
    except OSError:
        print("Baseline could not be checked safely; details withheld.", file=sys.stderr)
        return 2
    active_findings, suppressed = apply_baseline(findings, baseline_hashes)

    if args.json:
        print(json.dumps([public_finding(finding) for finding in active_findings], indent=2))
    else:
        print_text(active_findings, target, suppressed, baseline_path)

    return 1 if active_findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
