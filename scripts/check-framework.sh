#!/usr/bin/env bash
# Run structural integrity and meaningful probes in isolated temporary projects.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec python3 "$ROOT/scripts/check-framework.py" "$@"
