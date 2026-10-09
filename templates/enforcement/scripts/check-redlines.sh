#!/usr/bin/env bash
# Lexical smoke checks only: grep is not a complete syntax / semantic analyzer.
# Exit: 0 PASS, 1 violation, 2 configuration / scanner error. CI must block 1 and 2.
set -o pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
INCLUDES=(--include='*.ts' --include='*.tsx' --include='*.js' --include='*.py' --include='*.go')
EXCLUDES=(--exclude-dir=node_modules --exclude-dir=dist --exclude-dir=.git --exclude-dir=coverage --exclude-dir=vendor)

# Fill from the approved contract independently of the active checks.
EXPECTED_IDS=()

fail=0
error=0
seen=()
check() {
  if [ "$#" -lt 4 ]; then
    echo 'ERROR: check requires ID, message, pattern and explicit paths' >&2
    error=1; return
  fi
  local id="$1" msg="$2" pattern="$3"; shift 3
  local paths=("$@") hits status prior
  for prior in "${seen[@]}"; do
    if [ "$prior" = "$id" ]; then
      printf 'ERROR [%s]: duplicate rule\n' "$id" >&2; error=1; return
    fi
  done
  seen+=("$id")
  for path in "${paths[@]}"; do
    if [ ! -e "$path" ]; then
      printf 'ERROR [%s]: missing search path %s\n' "$id" "$path" >&2
      error=1; return
    fi
  done
  # grep 1 means no match; syntax / read / tool errors must remain errors.
  hits="$(grep -rnE "${INCLUDES[@]}" "${EXCLUDES[@]}" -- "$pattern" "${paths[@]}")"
  status=$?
  case "$status" in
    0) printf 'FAIL [%s]: %s\n%s\n' "$id" "$msg" "$hits"; fail=1 ;;
    1) ;;
    *) printf 'ERROR [%s]: grep exited %s\n' "$id" "$status" >&2; error=1 ;;
  esac
}
finish() {
  local expected active found
  if [ "${#EXPECTED_IDS[@]}" -eq 0 ]; then
    echo 'ERROR: no rules configured; declare EXPECTED_IDS and enable checks' >&2
    error=1
  fi
  for expected in "${EXPECTED_IDS[@]}"; do
    found=0
    for active in "${seen[@]}"; do [ "$active" != "$expected" ] || found=$((found + 1)); done
    if [ "$found" -ne 1 ]; then
      printf 'ERROR [%s]: expected one active check, got %s\n' "$expected" "$found" >&2; error=1
    fi
  done
  for active in "${seen[@]}"; do
    found=0
    for expected in "${EXPECTED_IDS[@]}"; do [ "$active" != "$expected" ] || found=$((found + 1)); done
    if [ "$found" -ne 1 ]; then
      printf 'ERROR [%s]: rule absent or duplicated in EXPECTED_IDS\n' "$active" >&2; error=1
    fi
  done
  [ "$error" -eq 0 ] || exit 2
  [ "$fail" -eq 0 ] || exit 1
  printf 'PASS: %s configured lexical checks\n' "${#seen[@]}"
}

# Enable project checks here; an unconfigured template intentionally exits 2.
# check "R1" "legacy dependency must use the approved replacement" "legacy-lib" src
finish
