# AGENTS.md — <PROJECT> Agent 协作契约

> 作者：<AUTHOR>　最近更新：<YYYY-MM-DD>
>
> 任何 AI 编码 agent（Claude Code / Codex / Cursor / Gemini CLI / 等）开始工作前必须读完本文。
>
> 本文是**入场指南**——告诉 agent 这个项目是什么、必读哪几份、不能碰什么、提交前必跑什么。
> 具体规则不在本文复述；在 [`HARNESS.md`](HARNESS.md)（工程契约）与 [`docs/`](docs/)。

<!--
占位符清单（拷过去后全局替换）：
  <PROJECT>     项目名
  <AUTHOR>      作者署名
  <MISSION>     项目使命一句话（最高优先级目标）
  <STACK>       一行技术栈
  <CI_CMD>      提交前必跑的 CI 命令串
标了 `> 示例（dw_gis3d）：` 的块是演示，填完请删。
-->

---

## 1. 项目一句话

<STACK>。
**使命：<MISSION>**——这条使命在任何阶段优先级 > 单个新功能。

> 示例（dw_gis3d）：Vue 3 + TS + Vite + 原生 Cesium + shadcn-vue。使命：彻底替代 frontend 对 HT 商业库的依赖。

## 2. 必读清单（按优先级）

| 优先级 | 文件 | 用途 |
| --- | --- | --- |
| P0 | [`README.md`](README.md) | 文档地图：按角色 / 任务找入口 |
| P0 | [`HARNESS.md`](HARNESS.md) | 工程契约：北极星 / 技术栈 / 目录 / **红线（§8）** |
| P0 | [`docs/SPEC.md`](docs/SPEC.md) | 业务规格总纲：用例索引 + 业务决议卡 |
| P0 | [`docs/workflow.md`](docs/workflow.md) | **按场景的工作流索引**——做事前先定位你属于哪一行 |
| P0 | [`docs/harness-controls.md`](docs/harness-controls.md) | Guide / Sensor / Behaviour evidence / Steering 控制台账 |
| P0 | [`docs/git-commit-conventions.md`](docs/git-commit-conventions.md) | commit 格式（commitlint 强制） |
| P1（按需） | [`docs/<模块>.md`](docs/) | 具体业务/契约文档 |
| P1（按需） | [`docs/adr/`](docs/adr/) | 已决决策记录 |

最小入场顺序：**README → workflow.md 找到对应场景 → HARNESS.md 红线 → 该场景指向的具体文档**。

## 3. 不可破的硬约束（违反立即停手并向用户报警）

1. **HARNESS.md §8 红线**全部驳回级。不要在 PR / 回应里讨论「我能不能例外」。
2. <把项目最核心的「碰即停」约束逐条列在这里，与 HARNESS 红线对齐>
3. **改契约要先开 ADR**：[`docs/adr/`](docs/adr/) 与 `HARNESS.md` 的实质改动不允许直接编辑既存文档；写新 ADR 标 `Supersedes`。

> 示例（dw_gis3d）：任何形式的 HT 引用都禁止（`import 'ht'` / `@hightopo/*` / `window.ht` / `ht.*`），命中即停。

## 4. 工作动作（每次任务必做）

### 4.1 干活前
- 在 [`docs/workflow.md`](docs/workflow.md) §1 找到对应场景行，读它指向的「先读哪份」与「必守红线」。
- 在 [`docs/harness-controls.md`](docs/harness-controls.md) 找到相关目标的 Guide、Sensor、失败处置和人工验收边界。
- 不在场景表里的任务，先和用户确认归属。

### 4.2 写代码
- 测试：新代码必须有单测；<如有特殊运行环境约束在此声明，例如 WebGL 走 Browser Mode 不走 jsdom>。
- 注释：解释思路与 why，不复述代码 what；作者署名 `<AUTHOR>`。
- 文件 > <N> 行视为重构信号（反 God-Class）。
- 单 PR 改动 > <M> 行视为拆分信号。

### 4.3 Git 操作
- `git add` **必须显式列文件**，禁止 `git add .` / `git add -A`。
- commit message 严格走 [`docs/git-commit-conventions.md`](docs/git-commit-conventions.md)。
- 禁止 `--no-verify` / `--no-gpg-sign`；禁止在主分支 force push（feature 分支仅 `--force-with-lease`）。
- 引入 `BREAKING CHANGE` 必须配 ADR。

### 4.4 提交前自查（全是「是」才能 request review）
1. 用例编号写进 PR 描述了？
2. 对应里程碑 DoD 勾了哪几条？
3. 红线全部清零？（grep 自查每条红线各一遍）
4. CI 全绿：`<CI_CMD>`
5. 触及新依赖 / 新契约 / 红线例外，ADR 起好了？
6. commit message 走了 conventions？
7. 相关 Sensor 跑过并能指导修复？关键 Behaviour 有独立验收证据？

## 5. 行为风格

- **<语言>回复**，关键术语保留英文。
- 探索性问题（「应该怎么做」）2–3 句给推荐 + 主要权衡，不直接动手；用户确认再实施。
- **改动外科手术式**：只动需要动的；不「顺手美化」邻居代码 / 注释 / 格式。
- 拿不准就停下来问，不要瞎猜。冲突的两个模式不要平均融合——选一个、说明为什么、把另一个标出来。
- 「Completed」只在所有验证都过之后才能说；任何步骤被跳过都要显式说明。
- 同类失败重复出现时，不只修当前代码：把证据写入 `docs/harness-controls.md` Steering Log，提议升级 Guide / Sensor，由 Owner 批准。

## 6. 跨 agent 配置约定

- `AGENTS.md`（本文）是**唯一契约源**。
- 其他 agent 配置文件（`CLAUDE.md` / `.cursorrules` / 等）应当只是指向本文的指针——不要让多个文件分头维护契约，一定会漂移。
- 如果你的 agent 不读 `AGENTS.md`，请在它的专属配置里加一行 `@AGENTS.md`（或等价语法）。
