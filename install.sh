#!/usr/bin/env bash
set -euo pipefail
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
for interpreter in python3 python; do
  if command -v "$interpreter" >/dev/null 2>&1 &&
     "$interpreter" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)' 2>/dev/null; then
    exec "$interpreter" -B "$repo_root/tools/install_skills.py" "$@"
  fi
done
echo "Python 3.11 or newer is required; no dependency is installed automatically." >&2
exit 1
