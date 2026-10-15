# AGENTS.md — <PROJECT> Agent 协作契约

<!-- harness:controls-read-policy=on-demand -->
<!-- harness:context-routing=progressive-and-probed -->

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
**使命：<MISSION>**。在用户当前范围和权限下维护该目标，方向实质变化由 Change Authority 决定。

> 示例（dw_gis3d）：Vue 3 + TS + Vite + 原生 Cesium + shadcn-vue。使命：彻底替代 frontend 对 HT 商业库的依赖。

## 2. 上下文路由表

| 优先级 | 文件 | 用途 |
| --- | --- | --- |
| Always-on | [`README.md`](README.md) | 文档地图：按角色 / 任务找入口 |
| Always-on | [`docs/workflow.md`](docs/workflow.md) | **按场景的工作流索引**——先定位你属于哪一行 |
| Always-on | [`HARNESS.md`](HARNESS.md) §0.0 / §8 | 当前方向、关闭证据与全局红线 |
| Task-loaded | [`docs/SPEC.md`](docs/SPEC.md) | 命中业务场景时读取对应规格与 Behaviour Evidence |
| Task-loaded | [`docs/harness-controls.md`](docs/harness-controls.md) | 仅在场景涉及软约束、人工边界、重复失败或 runner 时读取相关段 |
| Task-loaded | [`docs/<模块>.md`](docs/) / [`docs/adr/`](docs/adr/) | 只读当前路径 / 边界对应的 Owner Doc |
| Phase-loaded | [`docs/git-commit-conventions.md`](docs/git-commit-conventions.md) | 只在准备 commit 时载入 |

最小入场顺序：**README → workflow.md 找到对应场景 → HARNESS.md §0.0 / §8 → 该场景指向的具体文档**。不要求开工时通读 SPEC、Controls、全部 ADR 或提交规范。

Routing Probe：开工前确认“场景已命中、改动路径 / 边界有 Owner Doc、Closure Evidence 锚点可达”。在平台规则与用户当前指令之下，项目事实 / Owner Doc > Skills > memory / 建议性上下文；冲突时暴露冲突并停在该分支。

## 3. 硬约束与变更权限

1. **HARNESS.md §8 启用的阻断红线**必须通过。自身变更违反时自行修复并复验；缺少权限或事实冲突时只暂停依赖分支。观察模式和候选控制不能宣称已守门。
2. <只列最高风险约束的 Owner Doc 锚点，与 HARNESS 编号对齐，不复制规则正文>
3. **当前契约保持最新**：授权范围内更新 `HARNESS.md`。重大决策按项目要求新建 ADR；已合入 ADR 正文保持历史不变，推翻时用新 ADR 明确 `Supersedes`，同步当前契约。未采用 ADR 的组合删除该引用。

> 示例（dw_gis3d）：任何形式的 HT 引用都禁止（`import 'ht'` / `@hightopo/*` / `window.ht` / `ht.*`），命中即停。

## 4. 工作动作（每次任务必做）

### 4.1 干活前
- 在 [`docs/workflow.md`](docs/workflow.md) §1 找到对应场景行，读它指向的「先读哪份」与「必守红线」。
- 只有 workflow 场景指向控制台账，或任务涉及软约束、人工边界、重复失败时，才读取 [`docs/harness-controls.md`](docs/harness-controls.md) 的相关行。
- 场景未命中时，结合目标、改动路径和现有 Owner Doc 选择最近场景；只有实质事实或授权缺口无法消解时询问，继续不依赖答案的工作。

### 4.2 写代码
- 测试：按行为与风险选择验证；低风险文案不新增复述实现的测试；<如有特殊运行环境约束在此声明，例如 WebGL 走 Browser Mode 不走 jsdom>。
- 修复、子系统契约更新和审阅证据按 [`docs/workflow.md`](docs/workflow.md) §5；先确认实际运行路径，记录前后行为与验证版本。
- 注释：解释意图与约束，不复述实现；作者仅在项目要求时填写。
- 文件 > <N> 行视为重构信号（反 God-Class）。
- 单 PR 改动 > <M> 行视为拆分信号。

### 4.3 Git 操作
- `git add` **必须显式列文件**，禁止 `git add .` / `git add -A`。
- commit message 严格走 [`docs/git-commit-conventions.md`](docs/git-commit-conventions.md)。
- 禁止 `--no-verify` / `--no-gpg-sign`；禁止在主分支 force push（feature 分支仅 `--force-with-lease`）。
- 引入 `BREAKING CHANGE` 必须配 ADR。

### 4.4 提交前自查（适用项通过；不适用项说明理由）
1. 涉及业务用例时，引用实际 Behaviour Owner Doc 的验收条目了？
2. 涉及已设里程碑时，相关 DoD 达成了吗？
3. 启用的阻断控制通过？Legacy 已批准 baseline 无新增违规且未静默扩大？
4. 必要的项目检查通过：`<CI_CMD>`；错误、失败、未运行分别报告。
5. 涉及重大决策时，项目要求的 ADR / 授权已齐备？
6. commit message 走了 conventions？
7. 相关 Sensor 跑过并能指导修复？关键 Behaviour 有独立验收证据？

## 5. 行为风格

- **<语言>回复**，关键术语保留英文。
- 探索性问题（「应该怎么做」）2–3 句给推荐 + 主要权衡，不直接动手；用户确认再实施。
- **改动外科手术式**：只动需要动的；不「顺手美化」邻居代码 / 注释 / 格式。
- 先查现有证据，合理可逆细节自行决定；实质业务语义或授权缺口无法推断时才问。冲突的两个模式不要平均融合——选一个、说明为什么、把另一个标出来。
- 「Completed」只在所有验证都过之后才能说；任何步骤被跳过都要显式说明。
- 单次普通失败只修当前问题。同类失败至少两次，或一次高严重度逃逸时，按 `docs/harness-controls.md` 生成 Candidate；先分类、回放原失败并跑反例 / 路由 smoke，再由 Owner 决定是否升级 Guide / Sensor / Skill / Gate。自主提出的 Candidate 不得自动覆盖正式契约或 Skill；用户已明确授权维护该对象时直接修改并验证，不重复求批准。

## 6. 跨 agent 配置约定

- `AGENTS.md`（本文）是**唯一项目入口**，规则分别由指定 Owner Doc 持有。
- 其他 agent 配置文件（`CLAUDE.md` / `.cursorrules` / 等）应当只是指向本文的指针——不要让多个文件分头维护契约，一定会漂移。
- 如果你的 agent 不读 `AGENTS.md`，请在它的专属配置里加一行 `@AGENTS.md`（或等价语法）。
