---
name: harness-framework
description: Use when 给新项目铺设、给已有代码库接入、或增量维护 AI agent 工程契约（AGENTS.md / redline / Guide / Sensor / Context Routing / Experience Promotion / 提交规范），让 Claude Code、Codex、Cursor、Gemini 等 agent 进场即知边界、只加载当前所需事实、做完可自修，并把重复纠正经过评测后晋级为 Skill 或控制。触发场景：新项目脚手架、给项目立规矩、维护或升级已有 Harness、修改红线 / Guide / Sensor / agent 薄指针、agent 反复踩同样的坑、把工程经验沉淀成 Skill、上下文太重或经常漏读、接 Codex Goal / Mission Driver 等 runner、文档即契约 / docs-as-contract。
---

# Harness Framework —— 文档即契约协作脚手架

## 这是什么
把项目的「钢印级约束」固化成可索引的 Guides，把关键风险编译成可执行的 Sensors，
让任意 AI 编码 agent 进场即知边界、只装入当前任务所需上下文、做完能自我修正，
并让稳定经验经过 Evidence → Candidate → Eval → Owner 后才晋级为 Guide、Sensor、Skill 或 Gate。
基于 `AGENTS.md` 开放标准（一份真契约 + 各工具薄指针），与技术栈无关。

## 何时用
- 新项目要一次性铺好 agent 契约骨架
- 已有项目要接入 agent 约束但不破坏现状
- 已接入项目要增量维护 Redline、Guide、Sensor、Behaviour 或 AI-facing 入口
- 要把重复人工纠正或审计漏检沉淀成可复用 Skill / Sensor，但不希望自动堆规则
- 要让 Codex Goal、Mission Driver 等 runner 消费项目契约，而不让 runner 反客为主
- 迁移/替换项目要禁止旧依赖复活
- 症状：每个会话都在重复解释项目规矩；agent 反复踩同样的坑、长会话里「就这一次」破例

## 不适用
- 一次性脚本、玩具项目（连 AGENTS.md 都不必要）
- 已有成熟 agent 契约且无痛点

## 首次接入流程（八步，**负向验证与 Behaviour evidence 不可跳**）
先读 `AI-ADOPTION-PROTOCOL.md` 拿完整口径与「给 AI 的固定指令」，按此执行：

1. **Project Audit + Direction** — 识别技术栈、边界、历史债和行为证据；在 HARNESS §0.0 冻结基线、目标、不变量 / 非目标、关闭证据与变更权限
2. **Context Routing + Instantiate** — 定义 always-on / task-loaded / phase-loaded 路由和 Probe，再实例化必要契约；不新增日常动作
3. **Control Map** — 最小登记 Guide、Sensor / 人工确认、失败处置与 Owner；疑难项才追加类型和生命周期
4. **Redline Design** — 提炼 3-8 条**可机械检查**的红线，登记到 HARNESS §8
5. **Enforcement** — 每条红线接 grep / lint / commitlint / CI 守门（机制 2.5）
6. **Negative Verification + Self-correction** — 违规探针确认失败且反馈可修；删探针再确认通过
7. **Behaviour Evidence** — 在 SPEC 登记关键用例的独立证据与人类验收边界；Controls 只引用
8. **Handoff + Experience Promotion** — 输出覆盖边界、控制、验证与待决；重复失败或高严重度逃逸只生成 Candidate，经反例评测和 Owner 批准后再晋级

## 首次接入 vs 增量维护
- **新项目**：直接铺完整骨架，红线先保守写 3-5 条。判据见 protocol「新项目执行口径」。
- **旧项目**：**不覆盖**已有 README/AGENTS/CLAUDE/GEMINI/CI；冲突生成候选文件（如 `HARNESS.harness-new.md`）
  或最小合并；已存在违规列入历史债 baseline，**只拦新增**。判据见 protocol「旧项目执行口径」。
- **已接入项目**：不重跑八步实例化。按 protocol「已接入项目维护口径」只同步受影响的事实源、引用与控制；Gate 变更做负向校准。普通业务改动不触发 Harness 维护。

## 多工具入口（机制 0）
`AGENTS.md` 是唯一真契约。对不原生读它的工具放**薄指针**：Claude Code → `CLAUDE.md`、
Gemini CLI / Antigravity → `GEMINI.md`，内容只有一行 `@AGENTS.md` 导入。**指针只指，不写规则**。

项目实际存在 Agent 定义、Skills、编排器或工具专用规则时，才审计悬空引用、职责重叠与复用机会；不存在时跳过，不创建空台账。对具体且高影响的系统边界，Sensor 应验证 producer 实际输出 → contract / transform → consumer 预期，而不是分别证明两端存在。

## 上下文路由与经验晋级

- `AGENTS.md` 与 workflow 场景是稳定入口；在平台规则与用户当前指令之下，项目事实 / Owner Doc > Skills > memory / 建议性上下文。
- 开工时只加载 always-on、命中场景的 task-loaded，以及当前动作所需的 phase-loaded 文档；用路径 / 场景 / 证据锚点 Probe 检查漏载。
- 单次普通失败只修当前任务。重复至少两次，或一次高严重度逃逸，形成 Evidence Packet 并分类：项目事实进 SPEC / ADR，复用方法进 Candidate Skill，机械可拒模式进 Gate，语义漏检进 Sensor，重试 / 状态 / 幂等进普通代码。
- Agent 只能创建 Candidate，不得自动覆盖正式 Skill 或项目契约。晋级必须包含原失败回放、反例 / 非适用例、路由 smoke、Owner 批准和回滚条件。
- 只有检测到 runner 时才补 Consumption Contract：输入目标、范围、Guides、Sensors、关闭证据、权限和停止条件；输出状态、证据、失败 Sensor 与外部副作用。runner 不拥有项目事实，也不得降低门禁。

## 资源
- `templates/` — 拷到目标项目根目录，`*.template.md` 去掉 `.template`，替换 `<PROJECT>`/`<MISSION>` 等占位符
- `AI-ADOPTION-PROTOCOL.md` — 完整执行协议 + 给 AI 的固定指令 + 输出格式（**必读**）
- `INSTANTIATION-CHECKLIST.md` — 逐条勾的落地清单
- `METHODOLOGY.md` — 11 个机制为什么存在、如何按项目规模裁剪
- `docs/HARNESS-ENGINEERING.md` — Guides / Sensors / Context Routing / Experience Promotion 上位模型与边界
- `examples/node-orders-api/` — 异构完整样例（红线 grep 守门已验证可拦违规），照着看「填成什么样」

## 最关键的一条
机制 2.5（红线守门）不可跳过——**红线没有机械闸门就只是装饰**，制造「我们有规矩」的假象比没规矩更危险。
红线的黄金标准：**能写成一行 grep / lint 命令**。写不出命令的不是红线，降级到北极星原则或普通规范。

但写不出机械命令不代表不重要：语义与权衡登记为 Inferential Review Criterion，业务意图、风险和责任登记为 Human Acceptance Decision。关键 Behaviour 必须有独立证据，当前实现 agent 自生成的测试不能成为唯一验收依据。
