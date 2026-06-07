#!/usr/bin/env bash
# 红线 grep 守门 —— 与 HARNESS.md §8 一一对应，任一命中即 exit 1。
#
# 这是最跨语言、最不依赖工具链的红线闸门：哪怕项目没有 eslint，
# 一条 grep 也能把「碰即停」的约束变成机械拦截。CI 与 pre-commit 都调它。
#
# 用法：bash scripts/check-redlines.sh
# 退出码：0 = 全部清零；1 = 有红线被触发（合并应被拦下）
#
# @author <AUTHOR>
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

# 默认只扫源码类文件；按项目语言改这里
INCLUDES=(--include='*.ts' --include='*.tsx' --include='*.js' --include='*.vue' --include='*.py' --include='*.go')
EXCLUDES=(--exclude-dir=node_modules --exclude-dir=dist --exclude-dir=.git --exclude-dir=coverage --exclude-dir=vendor)

fail=0

# check <红线号> <说明> <ERE 模式> [搜索路径...]
#   命中任一行即记一笔失败，并打印命中位置（文件:行号:内容）。
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

# ── 在这里逐条登记你的红线（编号与 HARNESS §8 严格对齐）──────────────────
# 每条红线在 HARNESS §8 的「守门命令」列里就是下面这一行 check(...)。
# 填不出 grep 模式的「红线」不是红线——把它降级到北极星或普通规范。
#
# 示例（删掉换成你项目的）：
#   check "R2" "禁止类型逃逸 as any / as unknown" '\bas any\b|as unknown as' src
#   check "R5" "禁止引入第二套 UI 库"            "from ['\"](element-plus|naive-ui|antd)" src
#   check "R6" "被替换的旧依赖禁止复活"          "import .*['\"](legacy-lib|@old/.+)['\"]" src
#   check "R7" "业务层禁止裸 import 重依赖"       "from ['\"]heavydep(/|['\"])" src/modules
# ──────────────────────────────────────────────────────────────────────

# <在此粘贴你的 check 行>

if [ "$fail" -ne 0 ]; then
  echo ""
  echo "红线被触发，合并应被拦下。修掉上面的命中再提交。"
  exit 1
fi
echo "✓ 红线全部清零"
