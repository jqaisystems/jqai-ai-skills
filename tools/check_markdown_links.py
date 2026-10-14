#!/usr/bin/env python3
"""Check local inline Markdown file targets, excluding fenced code."""
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def targets(text):
    # Repository documentation uses inline links. Anchors and remote availability
    # are deliberately outside this offline file-existence check.
    lines = []
    fence = None
    for line in text.splitlines():
        match = re.match(r"^\s*([`~]{3,})", line)
        if match:
            char = match[1][0]
            if fence is None:
                fence = char
            elif fence == char:
                fence = None
            continue
        if fence is None:
            lines.append(line)
    text = "\n".join(lines)
    # Do not strip backticks inside link labels.
    for match in re.finditer(r"!?\[[^\]\n]*\]\((<[^>\n]+>|[^)\n]+)\)", text):
        target = match[1].strip()
        if target.startswith("<"):
            target = target[1:-1]
        else:
            target = re.split(r'\s+["\']', target, maxsplit=1)[0]
        parsed = urlsplit(target)
        if not parsed.scheme and not parsed.netloc and parsed.path:
            yield unquote(parsed.path)


def main():
    errors = []
    count = 0
    for file in sorted(ROOT.rglob("*.md")):
        relative = file.relative_to(ROOT)
        if any(part.startswith(".") or part in {"__pycache__", "node_modules"} for part in relative.parts):
            continue
        count += 1
        for target in targets(file.read_text(encoding="utf-8")):
            if not (file.parent / target).exists():
                errors.append(f"{relative.as_posix()}: missing {target}")
    if errors:
        print("\n".join(errors))
        return 1
    print(f"Checked local Markdown file links in {count} files (remote URLs and anchors not fetched).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
