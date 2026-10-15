---
name: harness-framework
description: "Set up or maintain project agent contracts, context routing, and verification gates when that maintenance is requested."
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

## 首次接入流程（仅用于已授权的项目 Harness 接入）

先确定需要维护的边界。普通规则审阅、机器级 Agent 环境维护或少量文案修订，不要求实例化项目骨架、建立新台账或新门禁。以下步骤按实际接入对象裁剪；新增/修改机械门禁时保留正负验证，关键行为的验收依据须独立于实现。
先读 `AI-ADOPTION-PROTOCOL.md` 拿完整口径与「给 AI 的固定指令」，按此执行：

1. **Project Audit + Direction** — 识别技术栈、边界、历史债和行为证据；在 HARNESS §0.0 冻结基线、目标、不变量 / 非目标、关闭证据与变更权限
2. **Context Routing + Instantiate** — 定义 always-on / task-loaded / phase-loaded 路由和 Probe，再实例化必要契约；不新增日常动作
3. **Control Map** — 最小登记 Guide、Sensor / 人工确认、失败处置与 Owner；疑难项才追加类型和生命周期
4. **Redline Design** — 从具体风险提炼必要且**可机械检查**的红线，不为凑数量新增约束，登记到 HARNESS §8
5. **Enforcement** — 每条红线接 grep / lint / commitlint / CI 守门（机制 2.5）
6. **Verification + Self-correction** — 合法 / 违规 / 错误探针确认 PASS / FAIL / ERROR；缺少配置或扫描器出错不能显示通过；删探针再复验
7. **Behaviour Evidence** — 在 SPEC 或实际 Behaviour Owner Doc 登记关键用例的独立证据与人类验收边界；Controls 只引用
8. **Handoff + Experience Promotion** — 输出覆盖边界、控制、验证与待决；重复失败或高严重度逃逸只生成 Candidate，自主候选经反例评测与对应授权后晋级；已有明确维护授权直接执行

## 首次接入 vs 增量维护
- **新项目**：按实际风险和已授权范围实例化必要骨架，红线数量由风险决定。判据见 protocol「新项目执行口径」。
- **旧项目**：**不覆盖**已有 README/AGENTS/CLAUDE/GEMINI/CI；冲突生成候选文件（如 `HARNESS.harness-new.md`）
  或最小合并；已存在违规列入历史债 baseline，**只拦新增**。判据见 protocol「旧项目执行口径」。
- **已接入项目**：不重跑八步实例化。按 protocol「已接入项目维护口径」只同步受影响的事实源、引用与控制；Gate 变更做负向校准。普通业务改动不触发 Harness 维护。

## 多工具入口（机制 0）
`AGENTS.md` 是唯一项目入口；事实由指定 Owner Doc 持有。对不原生读它的工具放**薄指针**：Claude Code → `CLAUDE.md`、
Gemini CLI / Antigravity → `GEMINI.md`，内容只有一行 `@AGENTS.md` 导入。**指针只指，不写规则**。

项目实际存在 Agent 定义、Skills、编排器或工具专用规则时，才审计悬空引用、职责重叠与复用机会；不存在时跳过，不创建空台账。对具体且高影响的系统边界，Sensor 应验证 producer 实际输出 → contract / transform → consumer 预期，而不是分别证明两端存在。

## 变更、修复与 Review

按 `docs/change-verification.md` 增量吸收：规划先确认实际执行路径，变更说明写触发条件与前后行为；复杂子系统可选 `templates/docs/subsystem.template.md`，已有 Owner Doc 就补在原处。行为修复验证旧实现的目标失败与新实现通过，搜索同类路径；无法安全回放时明示限制。普通任务与 runner 都将验证 / 审阅证据绑定实际代码和相关输入版本，变化后复验受影响部分。规则吸收到既有 workflow，不新增日常台账或固定全量测试要求；合并、发布仍需要对应授权。

## 上下文路由与经验晋级

- `AGENTS.md` 与 workflow 场景是稳定入口；在平台规则与用户当前指令之下，项目事实 / Owner Doc > Skills > memory / 建议性上下文。
- 开工时只加载 always-on、命中场景的 task-loaded，以及当前动作所需的 phase-loaded 文档；用路径 / 场景 / 证据锚点 Probe 检查漏载。
- 单次普通失败只修当前任务。重复至少两次，或一次高严重度逃逸，形成 Evidence Packet 并分类：项目事实进 SPEC / ADR，复用方法进 Candidate Skill，机械可拒模式进 Gate，语义漏检进 Sensor，重试 / 状态 / 幂等进普通代码。
- 在普通业务任务中自行发现的经验先成为 Candidate，不自动修改正式 Skill 或项目契约。用户明确要求维护这些文件时，按已授权范围直接修改、验证并保留回滚，不把 Candidate 流程变成重复批准。改变共享契约或发布范围仍需相应 Owner 授权；正式经验晋级保留原失败回放、反例和路由验证。
- 达到经验触发条件后，用薄索引和主题条目按任务召回；稳定 ID 与 candidate / evaluated / active / retired 状态保留历史。正式规则只在一个事实源维护，Skill 效果用同条件有 / 无 Skill 评测，失效经验退役。
- 只有检测到 runner 时才补 Consumption Contract：输入目标、范围、Guides、Sensors、关闭证据、权限和停止条件；输出状态、证据、失败 Sensor 与外部副作用。runner 不拥有项目事实，也不得降低门禁。

## 资源
- `templates/` — 按所选组合复制必要文件，`*.template.md` 去掉 `.template`，替换 `<PROJECT>`/`<MISSION>` 等占位符
- `AI-ADOPTION-PROTOCOL.md` — 完整执行协议 + 给 AI 的固定指令 + 输出格式（**必读**）
- `INSTANTIATION-CHECKLIST.md` — 逐条勾的落地清单
- `METHODOLOGY.md` — 11 个机制为什么存在、如何按项目规模裁剪
- `docs/HARNESS-ENGINEERING.md` — Guides / Sensors / Context Routing / Experience Promotion 上位模型与边界
- `docs/instantiation-profiles.md` — minimal / product 与旧项目增量合并；裁剪后引用须闭合
- `docs/change-verification.md` — 实际运行路径、回归证明、版本证据与按风险记录的环境覆盖
- `docs/experience-learning.md` — 首次失败索引、按任务召回、状态、Skill A/B、退役
- `examples/experience-loop/` — 本仓真实扫描错误假绿的旧 / 新回放；模型 A/B 未运行
- `examples/node-orders-api/` — 假想业务的字段示例，grep 是有限 smoke，业务 fixtures / CI 未实现
- `scripts/validate-instantiation.py` — 实例化文档与锚点检查，不代替语义验收
- `scripts/check-baseline.py` — 只拦新增的文本 baseline；保留重复计数，扫描错误阻断

## 最关键的一条
机制 2.5（红线守门）不可跳过——**红线没有机械闸门就只是装饰**，制造「我们有规矩」的假象比没规矩更危险。
红线必须可稳定机械判断，并经过合法 / 违规 / 错误验证。grep 是有限文本 smoke；静态 import lint 不自动覆盖动态引用，不夸大检测保证。写不出命令的不是红线，降级到北极星原则或普通规范。

但写不出机械命令不代表不重要：语义与权衡登记为 Inferential Review Criterion，业务意图、风险和责任登记为 Human Acceptance Decision。关键 Behaviour 必须有独立证据，当前实现 agent 自生成的测试不能成为唯一验收依据。
