#!/usr/bin/env bash
set -euo pipefail

skill="web-scraper"
target="${HOME}/.codex/skills"
install_all=0
list_only=0

usage() {
  cat <<'EOF'
Usage:
  ./install.sh [skill-name]
  ./install.sh --all
  ./install.sh --list
  ./install.sh --target /path/to/skills skill-name

Examples:
  ./install.sh web-scraper
  ./install.sh release-announcement-writer
  ./install.sh --all
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --all)
      install_all=1
      shift
      ;;
    --list)
      list_only=1
      shift
      ;;
    --target)
      target="${2:-}"
      if [[ -z "$target" ]]; then
        echo "Missing value for --target" >&2
        exit 1
      fi
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      skill="$1"
      shift
      ;;
  esac
done

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
skills_root="${repo_root}/skills"

if [[ ! -d "$skills_root" ]]; then
  echo "Could not find skills folder at ${skills_root}" >&2
  exit 1
fi

public_skills() {
  find "$skills_root" -mindepth 1 -maxdepth 1 -type d \
    ! -name "_template" \
    -exec test -f "{}/SKILL.md" \; -print |
    sort
}

if [[ "$list_only" -eq 1 ]]; then
  public_skills | xargs -n 1 basename
  exit 0
fi

mkdir -p "$target"

if [[ "$install_all" -eq 1 ]]; then
  mapfile -t selected < <(public_skills)
else
  selected=("${skills_root}/${skill}")
fi

for source in "${selected[@]}"; do
  if [[ ! -f "${source}/SKILL.md" ]]; then
    echo "Skill '$(basename "$source")' was not found. Available skills:" >&2
    public_skills | xargs -n 1 basename >&2
    exit 1
  fi
  destination="${target}/$(basename "$source")"
  rm -rf "$destination"
  cp -R "$source" "$destination"
  echo "Installed $(basename "$source") -> $destination"
done

echo "Restart Codex or reload your AI coding tool so the skill list refreshes."
