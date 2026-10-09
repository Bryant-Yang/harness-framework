#!/usr/bin/env bash
# node-orders-api 红线 grep 守门（填好版样例）—— 与 HARNESS-redlines.md 一一对应。
# 这是 templates/enforcement/scripts/check-redlines.sh 填实后的样子。
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

INCLUDES=(--include='*.ts')
EXCLUDES=(--exclude-dir=node_modules --exclude-dir=dist --exclude-dir=.git --exclude-dir=coverage)

fail=0
check() {
  local id="$1" msg="$2" pattern="$3"; shift 3
  local paths=("$@"); [ ${#paths[@]} -eq 0 ] && paths=(".")
  local missing=0
  for path in "${paths[@]}"; do
    if [ ! -e "$path" ]; then
      printf '✗ [%s] %s\n' "$id" "$msg"
      printf '      搜索路径不存在：%s\n' "$path"
      missing=1
      fail=1
    fi
  done
  [ "$missing" -ne 0 ] && return

  local hits
  hits="$(grep -rnE "${INCLUDES[@]}" "${EXCLUDES[@]}" "$pattern" "${paths[@]}" 2>/dev/null || true)"
  if [ -n "$hits" ]; then
    printf '✗ [%s] %s\n' "$id" "$msg"
    printf '%s\n' "$hits" | sed 's/^/      /'
    fail=1
  fi
}

# ── 与 HARNESS-redlines.md 编号严格对齐 ──────────────────────────────
check "R1" "domain/ 禁止 import prisma（DB 只能从 db/ 进）" "from ['\"]@?prisma" src/domain
check "R2" "被拆分的旧单体禁止复活" "@acme/monolith" src
check "R3" "禁止类型逃逸 as any / as unknown" '\bas any\b|as unknown as' src
check "R4" "禁止裸 process.env，走 config/env.ts" "process\.env\." src/services src/domain src/routes
check "R5" "禁止 console.log，走 logger" "console\.(log|debug)" src
check "R6" "路由层禁止裸 SQL 字符串" "(SELECT|INSERT|UPDATE|DELETE)[[:space:]]" src/routes
# R7（覆盖率）走 CI，R8（commit）走 commitlint —— 不是 grep 能查的，不放这里
# ────────────────────────────────────────────────────────────────────

if [ "$fail" -ne 0 ]; then
  echo ""
  echo "红线被触发，合并应被拦下。"
  exit 1
fi
echo "✓ 红线全部清零"
