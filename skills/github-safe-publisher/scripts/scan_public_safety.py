#!/usr/bin/env python3
"""Scan a public-release candidate for common safety risks."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
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
    ("token-like secret", re.compile(r"\b(?:sk|ghp|github_pat|xoxb|xoxp|AIza)[A-Za-z0-9_\-]{16,}\b"), "block"),
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


def is_probably_binary(path: Path) -> bool:
    try:
        chunk = path.read_bytes()[:4096]
    except OSError:
        return False
    return b"\0" in chunk


def iter_files(root: Path):
    if root.is_file():
        yield root
        return

    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file():
            yield path


def relative(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def scan_file(path: Path, root: Path) -> list[Finding]:
    findings: list[Finding] = []
    rel = relative(path, root)
    lower_name = path.name.lower()
    suffixes = {suffix.lower() for suffix in path.suffixes}

    if lower_name in RISKY_FILENAMES:
        findings.append(Finding("block", rel, None, "risky filename", path.name))

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
        except OSError as exc:
            findings.append(Finding("review", rel, None, "read error", str(exc)))
            return findings
    except OSError as exc:
        findings.append(Finding("review", rel, None, "read error", str(exc)))
        return findings

    for line_number, line in enumerate(text.splitlines(), start=1):
        for label, pattern, severity in CONTENT_PATTERNS:
            if pattern.search(line):
                snippet = line.strip()
                if len(snippet) > 140:
                    snippet = snippet[:137] + "..."
                findings.append(Finding(severity, rel, line_number, label, snippet))

    return findings


def scan(root: Path) -> list[Finding]:
    resolved = root.resolve()
    return [finding for path in iter_files(resolved) for finding in scan_file(path, resolved)]


def print_text(findings: list[Finding], target: Path) -> None:
    print(f"Public safety scan: {target}")
    if not findings:
        print("READY: no common safety risks found.")
        return

    block_count = sum(1 for finding in findings if finding.severity == "block")
    review_count = sum(1 for finding in findings if finding.severity == "review")
    verdict = "BLOCK" if block_count else "REVIEW"
    print(f"{verdict}: {block_count} blocking finding(s), {review_count} review finding(s).")

    for finding in findings:
        location = finding.path if finding.line is None else f"{finding.path}:{finding.line}"
        detail = finding.detail.encode("ascii", errors="backslashreplace").decode("ascii")
        print(f"- [{finding.severity}] {location} - {finding.kind}: {detail}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scan a public GitHub release candidate for safety risks.")
    parser.add_argument("target", help="File or folder to scan")
    parser.add_argument("--json", action="store_true", help="Print structured JSON findings")
    args = parser.parse_args(argv)

    target = Path(args.target)
    if not target.exists():
        print(f"Target does not exist: {target}", file=sys.stderr)
        return 2

    findings = scan(target)
    if args.json:
        print(json.dumps([asdict(finding) for finding in findings], indent=2))
    else:
        print_text(findings, target)

    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
