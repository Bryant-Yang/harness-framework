#!/usr/bin/env bash
# 把 harness-framework skill 从本仓库（唯一源）组装并安装到各 agent 的个人技能目录。
# 安装产物 = SKILL.md + templates/ + examples/ + 四份方法文档。
# 改了仓库里的源文件后重跑本脚本即可同步，缓解「自包含两份漂移」。
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_NAME="harness-framework"

# 目标：Claude Code 与 Codex 的个人技能目录。缺省可用环境变量覆盖根路径。
TARGETS=(
  "${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}/$SKILL_NAME"
  "${CODEX_SKILLS_DIR:-$HOME/.agents/skills}/$SKILL_NAME"
)

assemble() {
  local dest="$1"
  # 只清理本 skill 自己的目录，绝不动同级其它 skill
  rm -rf "$dest"
  mkdir -p "$dest/docs"

  cp "$ROOT/SKILL.md" "$dest/SKILL.md"
  cp -R "$ROOT/templates" "$dest/templates"
  cp -R "$ROOT/examples" "$dest/examples"
  cp "$ROOT/AI-ADOPTION-PROTOCOL.md" "$dest/AI-ADOPTION-PROTOCOL.md"
  cp "$ROOT/INSTANTIATION-CHECKLIST.md" "$dest/INSTANTIATION-CHECKLIST.md"
  cp "$ROOT/METHODOLOGY.md" "$dest/METHODOLOGY.md"
  cp "$ROOT/docs/HARNESS-ENGINEERING.md" "$dest/docs/HARNESS-ENGINEERING.md"

  echo "✓ 已安装：$dest"
}

for t in "${TARGETS[@]}"; do
  parent="$(dirname "$t")"
  if [ ! -d "$parent" ]; then
    echo "– 跳过（目标父目录不存在）：$parent"
    continue
  fi
  assemble "$t"
done

echo "完成。在 Claude Code / Codex 里即可发现 skill：$SKILL_NAME"
