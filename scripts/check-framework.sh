#!/usr/bin/env bash
# Harness Framework 自证检查：验证源仓库结构、版本/编号一致性、内部链接、薄指针、
# skill 组装声明和样例负向门禁。
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

required=(
  VERSION
  .github/workflows/check-framework.yml
  README.md
  METHODOLOGY.md
  AI-ADOPTION-PROTOCOL.md
  INSTANTIATION-CHECKLIST.md
  docs/HARNESS-ENGINEERING.md
  SKILL.md
  templates/AGENTS.template.md
  templates/HARNESS.template.md
  templates/docs/harness-controls.template.md
  templates/enforcement/scripts/check-redlines.sh
  examples/node-orders-api/harness-controls.md
  examples/node-orders-api/SPEC.md
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
if [ "$version" != "2.2.0" ]; then
  printf '✗ VERSION 不符合当前发布契约：%s\n' "$version"
  exit 1
fi

for versioned in README.md docs/HARNESS-ENGINEERING.md templates/HARNESS.template.md templates/docs/harness-controls.template.md; do
  if ! grep -q "$version" "$versioned"; then
    printf '✗ 版本没有与 VERSION 对齐：%s\n' "$versioned"
    exit 1
  fi
done

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

if ! grep -q 'HARNESS-ENGINEERING.md' scripts/sync-skill.sh; then
  echo '✗ skill 组装没有覆盖 Harness Engineering 方法文档'
  exit 1
fi

if ! grep -q 'harness:maintenance-routing=delta-impact' AI-ADOPTION-PROTOCOL.md ||
   ! grep -q 'harness:ai-assets-audit=conditional' AI-ADOPTION-PROTOCOL.md ||
   ! grep -q 'harness:boundary-sensor=producer-contract-consumer' docs/HARNESS-ENGINEERING.md; then
  echo '✗ 增量维护、条件式资产审计或双端边界 Sensor 契约缺失'
  exit 1
fi

for marker in \
  'harness:context-routing=progressive-and-probed' \
  'harness:experience-promotion=candidate-first' \
  'harness:runner-consumption=optional'; do
  if ! grep -q "$marker" AI-ADOPTION-PROTOCOL.md ||
     ! grep -q "$marker" docs/HARNESS-ENGINEERING.md ||
     ! grep -q "$marker" templates/docs/harness-controls.template.md ||
     ! grep -q "$marker" examples/node-orders-api/harness-controls.md; then
    printf '✗ 2.2 契约标记缺失：%s\n' "$marker"
    exit 1
  fi
done

if ! grep -q 'harness:control-map=minimum' templates/docs/harness-controls.template.md ||
   ! grep -q 'harness:control-map=minimum' examples/node-orders-api/harness-controls.md ||
   grep -Eq '^\| ID \|.*(Guide 类型|Sensor 类型)' templates/docs/harness-controls.template.md; then
  echo '✗ Control Map 不再遵守最小必填契约'
  exit 1
fi

if ! grep -q 'harness:behaviour-evidence=canonical-source' templates/docs/SPEC.template.md ||
   ! grep -q 'harness:behaviour-evidence=canonical-source' examples/node-orders-api/SPEC.md ||
   ! grep -q 'harness:behaviour-evidence=spec-reference-only' templates/docs/harness-controls.template.md ||
   ! grep -q 'harness:behaviour-evidence=spec-reference-only' examples/node-orders-api/harness-controls.md ||
   grep -q '| 用例 / 风险 | 独立证据来源' templates/docs/harness-controls.template.md ||
   ! grep -Eq '^\| Behaviour .*SPEC\.md' templates/docs/harness-controls.template.md ||
   ! grep -Eq '^\| Behaviour .*SPEC\.md' examples/node-orders-api/harness-controls.md; then
  echo '✗ Controls 与 SPEC 仍在双写 Behaviour Evidence'
  exit 1
fi

if ! grep -q 'harness:controls-read-policy=on-demand' templates/AGENTS.template.md ||
   ! grep -q 'harness:controls-read-policy=on-demand' examples/node-orders-api/AGENTS.md ||
   ! grep -q 'harness:context-routing=progressive-and-probed' templates/AGENTS.template.md ||
   ! grep -q 'harness:context-routing=progressive-and-probed' examples/node-orders-api/AGENTS.md ||
   ! grep -q '在平台规则与用户当前指令之下' templates/AGENTS.template.md ||
   ! grep -q '在平台规则与用户当前指令之下' templates/docs/workflow.template.md ||
   grep -Eq '^\| (P0|Always-on) \|.*(SPEC\.md|harness-controls\.md|git-commit-conventions\.md)' templates/AGENTS.template.md; then
  echo '✗ Context Routing 没有渐进加载，或任务 / 阶段资料仍被设为 Always-on'
  exit 1
fi

if ! grep -q 'harness:experience-trigger=repeat-2-or-high-severity-1' templates/docs/harness-controls.template.md ||
   ! grep -q 'harness:experience-trigger=repeat-2-or-high-severity-1' examples/node-orders-api/harness-controls.md ||
   grep -q '^| 日期 |' templates/docs/harness-controls.template.md; then
  echo '✗ Experience Promotion 没有采用事件触发，或模板仍强制空记录'
  exit 1
fi

if ! grep -q '当前基线' templates/HARNESS.template.md ||
   ! grep -q 'Closure Evidence' templates/HARNESS.template.md ||
   ! grep -q 'Change Authority' templates/HARNESS.template.md ||
   ! grep -q 'Agent 不得自动覆盖正式 Skill' templates/docs/harness-controls.template.md ||
   ! grep -q '没有 Codex Goal、Mission Driver 或外部 runner' examples/node-orders-api/harness-controls.md; then
  echo '✗ Direction Contract、Candidate-first 或可选 Runner 边界缺失'
  exit 1
fi

if [ "$(wc -l < SKILL.md)" -gt 500 ] ||
   ! grep -q '^name: harness-framework$' SKILL.md ||
   ! grep -q 'AI-ADOPTION-PROTOCOL.md' SKILL.md ||
   ! grep -q 'docs/HARNESS-ENGINEERING.md' SKILL.md; then
  echo '✗ 根目录 Skill 不是可发现、自包含的标准入口'
  exit 1
fi

if ! grep -q 'bash scripts/check-framework.sh' .github/workflows/check-framework.yml; then
  echo '✗ 仓库 CI 没有执行框架自证'
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

for doc in README.md METHODOLOGY.md docs/HARNESS-ENGINEERING.md examples/node-orders-api/README.md examples/node-orders-api/harness-controls.md; do
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
  "$sync_root/codex/harness-framework/docs/HARNESS-ENGINEERING.md" \
  "$sync_root/codex/harness-framework/templates/docs/harness-controls.template.md" \
  "$sync_root/codex/harness-framework/examples/node-orders-api/harness-controls.md"; do
  if [ ! -f "$assembled" ]; then
    printf '✗ skill 组装缺少 2.2 资源：%s\n' "$assembled"
    exit 1
  fi
done
if ! grep -q 'harness:maintenance-routing=delta-impact' "$sync_root/codex/harness-framework/AI-ADOPTION-PROTOCOL.md" ||
   ! grep -q 'harness:experience-promotion=candidate-first' "$sync_root/codex/harness-framework/docs/HARNESS-ENGINEERING.md"; then
  echo '✗ skill 组装没有携带 2.2 维护与经验晋级契约'
  exit 1
fi
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
