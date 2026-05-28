#!/usr/bin/env python3
"""Build a safe Markdown research brief skeleton from JSON records."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path
from typing import Any


VISIBILITY = {"public_ready", "needs_review", "private_research", "archive"}
RISKY_PATTERN = re.compile(
    r"(?i)([A-Z]:[\\/](?:Users|Documents and Settings)[\\/]|/(?:Users|home)/|"
    r"\b(api[_-]?key|secret|password|passwd|token|bearer|cookie|private[_-]?key)\b|"
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----)"
)


def load_items(path: Path | None) -> list[dict[str, Any]]:
    if path is None:
        return []
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, list):
        raise SystemExit("Input JSON must be a list of item records.")
    return [item if isinstance(item, dict) else {"title": str(item)} for item in data]


def clean(value: Any) -> str:
    return str(value or "").strip()


def visibility(item: dict[str, Any]) -> str:
    raw = clean(item.get("visibility") or item.get("status")).lower().replace("-", "_")
    return raw if raw in VISIBILITY else "needs_review"


def risky_fields(item: dict[str, Any]) -> list[str]:
    risky: list[str] = []
    for key, value in item.items():
        text = clean(value)
        if text and RISKY_PATTERN.search(text):
            risky.append(key)
    return risky


def item_line(item: dict[str, Any]) -> str:
    title = clean(item.get("title")) or "Untitled item"
    source = clean(item.get("source")) or "Source not provided"
    url = clean(item.get("url"))
    topic = clean(item.get("topic")) or "General"
    summary = clean(item.get("summary")) or "Summary pending human review."
    why = clean(item.get("why_it_matters")) or clean(item.get("why")) or "Relevance pending review."
    action = clean(item.get("next_action")) or clean(item.get("decision")) or "Review before reuse."
    source_text = f"[{source}]({url})" if url else source
    return (
        f"### {title}\n\n"
        f"- Source: {source_text}\n"
        f"- Topic: {topic}\n"
        f"- Summary: {summary}\n"
        f"- Why it matters: {why}\n"
        f"- Next action: {action}\n"
    )


def held_line(item: dict[str, Any]) -> str:
    title = clean(item.get("title")) or "Untitled item"
    reason = clean(item.get("review_note")) or clean(item.get("decision")) or "Needs human review."
    return f"- {title}: {reason}"


def build_markdown(items: list[dict[str, Any]], title: str, brief_date: str, audience: str) -> str:
    groups = {name: [] for name in sorted(VISIBILITY)}
    risk_notes: list[str] = []

    for item in items:
        risks = risky_fields(item)
        if risks:
            risk_notes.append(f"- {clean(item.get('title')) or 'Untitled item'}: risky fields {', '.join(risks)}")
            groups["needs_review"].append(item)
        else:
            groups[visibility(item)].append(item)

    verdict = "REVIEW" if risk_notes or groups["needs_review"] or groups["private_research"] else "READY"

    lines = [
        f"# {title}",
        "",
        f"Date: {brief_date}",
        f"Audience: {audience}",
        f"Sources reviewed: {len(items)}",
        f"Safety verdict: {verdict}",
        "",
        "## Executive Summary",
        "",
        "Review the public-ready items below, verify sources, and approve wording before sharing.",
        "",
        "## Public-Ready Highlights",
        "",
    ]

    public_items = groups["public_ready"]
    lines.append("\n".join(item_line(item) for item in public_items).strip() or "- No public-ready items yet.")
    lines.extend(["", "## Needs Review", ""])
    held = [held_line(item) for item in groups["needs_review"]]
    if risk_notes:
        held.extend(risk_notes)
    lines.append("\n".join(held) or "- No items currently need review.")
    lines.extend(["", "## Private Research / Archive", ""])
    private_archive = [held_line(item) for item in groups["private_research"] + groups["archive"]]
    lines.append("\n".join(private_archive) or "- No private or archived items listed.")
    lines.extend(
        [
            "",
            "## Manual Checks",
            "",
            "- Confirm all source links are public.",
            "- Confirm claims are supported by sources.",
            "- Remove private notes, raw prompts, logs, datasets, credentials, and local paths.",
            "- Approve wording before publishing, sending, or adding to a public repo.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a Markdown research brief skeleton from JSON records.")
    parser.add_argument("input", nargs="?", help="JSON file containing a list of item records.")
    parser.add_argument("--title", default="Research Brief")
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--audience", default="Internal review")
    parser.add_argument("--output", help="Optional output Markdown path. Prints to stdout when omitted.")
    args = parser.parse_args()

    items = load_items(Path(args.input) if args.input else None)
    markdown = build_markdown(items, args.title, args.date, args.audience)

    if args.output:
        Path(args.output).write_text(markdown, encoding="utf-8")
    else:
        print(markdown, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
