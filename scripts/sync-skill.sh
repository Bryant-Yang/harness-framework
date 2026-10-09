#!/usr/bin/env bash
# Package the maintained source, including docs/HARNESS-ENGINEERING.md.
# Python installer stages resources, preserves shared aliases, and keeps rollback backups.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec python3 "$ROOT/scripts/install-skill.py" "$@"
