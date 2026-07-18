#!/usr/bin/env bash
# Harness Framework 自证检查：验证源仓库结构、版本/编号一致性、内部链接、薄指针、
# skill 组装声明和样例负向门禁。
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

required=(
  VERSION
  README.md
  METHODOLOGY.md
  AI-ADOPTION-PROTOCOL.md
  INSTANTIATION-CHECKLIST.md
  docs/HARNESS-ENGINEERING.md
  skill/SKILL.md
  templates/AGENTS.template.md
  templates/HARNESS.template.md
  templates/docs/harness-controls.template.md
  templates/enforcement/scripts/check-redlines.sh
  examples/node-orders-api/harness-controls.md
)

for path in "${required[@]}"; do
  if [ ! -f "$path" ]; then
    printf '✗ 缺少必需文件：%s\n' "$path"
    exit 1
  fi
done

if grep -R -nE '<(PROJECT|AUTHOR|MISSION|CI_CMD|OWNER|DATE)>' examples/node-orders-api >/dev/null; then
  echo '✗ node-orders-api 示例仍残留模板占位符'
  exit 1
fi

version="$(tr -d '[:space:]' < VERSION)"
if [ "$version" != "2.0.0" ]; then
  printf '✗ VERSION 不符合当前发布契约：%s\n' "$version"
  exit 1
fi

for versioned in README.md docs/HARNESS-ENGINEERING.md templates/HARNESS.template.md templates/docs/harness-controls.template.md; do
  if ! grep -q "$version" "$versioned"; then
    printf '✗ 版本没有与 VERSION 对齐：%s\n' "$versioned"
    exit 1
  fi
done

if ! grep -q '11 个可复用机制' README.md ||
   ! grep -q '本文解释 11 个机制' METHODOLOGY.md ||
   ! grep -q '11 个机制' skill/SKILL.md; then
  echo '✗ README / METHODOLOGY / skill 的机制数量漂移'
  exit 1
fi

if ! grep -q '核心流程（八步' skill/SKILL.md || ! grep -q '^8\. Handoff + Steering' AI-ADOPTION-PROTOCOL.md; then
  echo '✗ skill 与 AI protocol 的八步流程漂移'
  exit 1
fi

if grep -Eq 'workflow §4|workflow.*§4' templates/enforcement/ci.yml templates/docs/deps-and-configs.template.md templates/PROJECT-README.template.md; then
  echo '✗ workflow 章节引用仍指向旧 §4'
  exit 1
fi

for pointer in templates/CLAUDE.md templates/GEMINI.md templates/.github/copilot-instructions.md templates/.cursor/rules/000-agents.mdc; do
  if ! grep -q 'AGENTS.md' "$pointer"; then
    printf '✗ 薄指针没有指回 AGENTS.md：%s\n' "$pointer"
    exit 1
  fi
  if grep -q '^## ' "$pointer" || [ "$(wc -l < "$pointer")" -gt 20 ]; then
    printf '✗ 跨 agent 文件不再是薄指针：%s\n' "$pointer"
    exit 1
  fi
done

if ! grep -q 'HARNESS-ENGINEERING.md' scripts/sync-skill.sh ||
   ! grep -q 'harness-controls.template.md' scripts/check-framework.sh; then
  echo '✗ skill 组装或自证清单没有覆盖 2.0 新资源'
  exit 1
fi

if ! grep -q 'Guide 类型.*Sensor 类型' templates/docs/harness-controls.template.md ||
   ! grep -q 'Guide 类型.*Sensor 类型' examples/node-orders-api/harness-controls.md; then
  echo '✗ Control Map 没有分别登记 Guide 与 Sensor 类型'
  exit 1
fi

if ! grep -q '关键 Behaviour 必填' templates/docs/SPEC.template.md; then
  echo '✗ SPEC 没有把独立证据限定在关键 Behaviour'
  exit 1
fi

check_links() {
  local doc="$1" raw link target
  while IFS= read -r raw; do
    link="${raw#](}"
    link="${link%)}"
    case "$link" in
      http://*|https://*|mailto:*|'#'*|*'<'*|*'>'*) continue ;;
    esac
    link="${link%%#*}"
    [ -z "$link" ] && continue
    target="$(dirname "$doc")/$link"
    if [ ! -e "$target" ]; then
      printf '✗ 内部链接目标不存在：%s → %s\n' "$doc" "$link"
      return 1
    fi
  done < <(grep -oE '\]\([^)]+\)' "$doc" || true)
}

for doc in README.md METHODOLOGY.md docs/HARNESS-ENGINEERING.md examples/node-orders-api/README.md; do
  check_links "$doc"
done

for id in R1 R2 R3 R4 R5 R6 R7 R8; do
  if ! grep -q "| $id |" examples/node-orders-api/HARNESS-redlines.md; then
    printf '✗ 样例红线表缺少 %s\n' "$id"
    exit 1
  fi
done

for id in R1 R2 R3 R4 R5 R6; do
  if ! grep -q "check \"$id\"" examples/node-orders-api/scripts/check-redlines.sh; then
    printf '✗ 样例红线脚本缺少 %s\n' "$id"
    exit 1
  fi
done

baseline_dir="$(mktemp -d)"
cleanup_baseline() { rm -rf "${baseline_dir:?}"; }
trap cleanup_baseline EXIT
printf 'src/legacy.ts:@acme/monolith\n' > "$baseline_dir/baseline.txt"
cp "$baseline_dir/baseline.txt" "$baseline_dir/current.txt"
if [ -n "$(comm -13 "$baseline_dir/baseline.txt" "$baseline_dir/current.txt")" ]; then
  echo '✗ Legacy baseline 把历史命中误判为新增'
  exit 1
fi
printf 'src/new.ts:@acme/monolith\n' >> "$baseline_dir/current.txt"
sort -o "$baseline_dir/current.txt" "$baseline_dir/current.txt"
if [ -z "$(comm -13 "$baseline_dir/baseline.txt" "$baseline_dir/current.txt")" ]; then
  echo '✗ Legacy baseline 没有识别新增命中'
  exit 1
fi
cleanup_baseline
trap - EXIT

sync_root="$(mktemp -d)"
cleanup_sync() { rm -rf "${sync_root:?}"; }
trap cleanup_sync EXIT
mkdir -p "$sync_root/claude" "$sync_root/codex"
CLAUDE_SKILLS_DIR="$sync_root/claude" CODEX_SKILLS_DIR="$sync_root/codex" bash scripts/sync-skill.sh >/dev/null
for assembled in \
  "$sync_root/codex/harness-framework/SKILL.md" \
  "$sync_root/codex/harness-framework/reference/HARNESS-ENGINEERING.md" \
  "$sync_root/codex/harness-framework/templates/docs/harness-controls.template.md" \
  "$sync_root/codex/harness-framework/examples/node-orders-api/harness-controls.md"; do
  if [ ! -f "$assembled" ]; then
    printf '✗ skill 组装缺少 2.0 资源：%s\n' "$assembled"
    exit 1
  fi
done
cleanup_sync
trap - EXIT

bash examples/node-orders-api/scripts/check-redlines.sh

tmp_base="$(mktemp "$ROOT/examples/node-orders-api/src/domain/.harness-negative-probe.XXXXXX")"
tmp_probe="${tmp_base}.ts"
mv "$tmp_base" "$tmp_probe"
cleanup() { rm -f "$tmp_probe"; }
trap cleanup EXIT
printf "import { PrismaClient } from '@prisma/client'\n" > "$tmp_probe"
if bash examples/node-orders-api/scripts/check-redlines.sh >/dev/null 2>&1; then
  echo '✗ 负向探针没有触发样例红线'
  exit 1
fi
cleanup
trap - EXIT
bash examples/node-orders-api/scripts/check-redlines.sh

echo '✓ Harness Framework 自证通过'
