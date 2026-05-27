#!/usr/bin/env python3
"""Validate public JQ AI skill folders and README-local asset links."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
README = ROOT / "README.md"


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening YAML frontmatter fence")

    try:
        end = next(i for i, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration as exc:
        raise ValueError("missing closing YAML frontmatter fence") from exc

    data: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def public_skill_dirs() -> list[Path]:
    return sorted(
        path
        for path in SKILLS.iterdir()
        if path.is_dir() and path.name != "_template"
    )


def validate_openai_yaml(skill_dir: Path, errors: list[str]) -> None:
    metadata = skill_dir / "agents" / "openai.yaml"
    if not metadata.exists():
        errors.append(f"{skill_dir}: missing agents/openai.yaml")
        return

    text = metadata.read_text(encoding="utf-8")
    required = ["display_name", "short_description", "default_prompt"]
    for key in required:
        if not re.search(rf"^\s*{re.escape(key)}\s*:\s*.+", text, re.MULTILINE):
            errors.append(f"{metadata}: missing interface.{key}")

    if f"${skill_dir.name}" not in text:
        errors.append(f"{metadata}: default_prompt should include ${skill_dir.name}")
    if "TODO" in text:
        errors.append(f"{metadata}: contains TODO placeholder")


def validate_skill(skill_dir: Path, readme_text: str, errors: list[str]) -> None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        errors.append(f"{skill_dir}: missing SKILL.md")
        return

    try:
        frontmatter = parse_frontmatter(skill_md)
    except ValueError as exc:
        errors.append(f"{skill_md}: {exc}")
        return

    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    if name != skill_dir.name:
        errors.append(f"{skill_md}: frontmatter name '{name}' must match folder '{skill_dir.name}'")
    if not description or len(description) < 40:
        errors.append(f"{skill_md}: description is missing or too short")

    text = skill_md.read_text(encoding="utf-8")
    if "TODO" in text:
        errors.append(f"{skill_md}: contains TODO placeholder")

    validate_openai_yaml(skill_dir, errors)

    expected_link = f"skills/{skill_dir.name}/SKILL.md"
    if expected_link not in readme_text:
        errors.append(f"README.md: missing link to {expected_link}")


def extract_local_markdown_targets(text: str) -> list[str]:
    targets = re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", text)
    local: list[str] = []
    for target in targets:
        clean = target.split("#", 1)[0].strip()
        if not clean or re.match(r"^[a-z]+://", clean) or clean.startswith("mailto:"):
            continue
        if clean.startswith("#"):
            continue
        local.append(clean)
    return local


def validate_readme_links(errors: list[str]) -> None:
    text = README.read_text(encoding="utf-8")
    for target in extract_local_markdown_targets(text):
        path = ROOT / target
        if not path.exists():
            errors.append(f"README.md: local target does not exist: {target}")


def main() -> int:
    errors: list[str] = []
    if not SKILLS.exists():
        errors.append("missing skills/ directory")
    if not README.exists():
        errors.append("missing README.md")

    readme_text = README.read_text(encoding="utf-8") if README.exists() else ""

    for skill_dir in public_skill_dirs():
        validate_skill(skill_dir, readme_text, errors)
    validate_readme_links(errors)

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validated {len(public_skill_dirs())} public skill folders.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
