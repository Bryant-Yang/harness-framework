---
name: harness-framework
description: Use when 给新项目铺设、或给已有代码库接入 AI agent 工程契约（AGENTS.md / 红线 redline / 提交规范），让 Claude Code、Codex、Cursor、Gemini 等 agent 进场即知项目边界、不可碰的红线、产出落点与提交前自查，而不必每个会话重新解释。触发场景：新项目脚手架、给项目立规矩、agent 反复踩同样的坑、每次会话都重复解释项目、想接 AGENTS.md / 红线 enforcement / 文档即契约 / docs-as-contract。
---

# Harness Framework —— 文档即契约协作脚手架

## 这是什么
把项目的「钢印级约束」固化成可索引的 Guides，把关键风险编译成可执行的 Sensors，
让任意 AI 编码 agent 进场即知边界、做完能自我修正、重复失败能进入 Human Steering。
基于 `AGENTS.md` 开放标准（一份真契约 + 各工具薄指针），与技术栈无关。

## 何时用
- 新项目要一次性铺好 agent 契约骨架
- 已有项目要接入 agent 约束但不破坏现状
- 迁移/替换项目要禁止旧依赖复活
- 症状：每个会话都在重复解释项目规矩；agent 反复踩同样的坑、长会话里「就这一次」破例

## 不适用
- 一次性脚本、玩具项目（连 AGENTS.md 都不必要）
- 已有成熟 agent 契约且无痛点

## 核心流程（八步，**负向验证与 Behaviour evidence 不可跳**）
先读 `reference/AI-ADOPTION-PROTOCOL.md` 拿完整口径与「给 AI 的固定指令」，按此执行：

1. **Project Audit + Harnessability** — 识别技术栈、边界、测试隔离性、反馈质量、历史债与行为证据
2. **Instantiate** — 实例化 AGENTS、HARNESS、workflow、harness-controls、commit 规范与必要指针
3. **Control Map** — 最小登记 Guide、Sensor / 人工确认、失败处置与 Owner；疑难项才追加类型和生命周期
4. **Redline Design** — 提炼 3-8 条**可机械检查**的红线，登记到 HARNESS §8
5. **Enforcement** — 每条红线接 grep / lint / commitlint / CI 守门（机制 2.5）
6. **Negative Verification + Self-correction** — 违规探针确认失败且反馈可修；删探针再确认通过
7. **Behaviour Evidence** — 在 SPEC 登记关键用例的独立证据与人类验收边界；Controls 只引用
8. **Handoff + Steering** — 输出覆盖边界、控制、验证、baseline 与人工待决；达到重复失败触发条件时才输出 Steering

## 新项目 vs 旧项目
- **新项目**：直接铺完整骨架，红线先保守写 3-5 条。判据见 protocol「新项目执行口径」。
- **旧项目**：**不覆盖**已有 README/AGENTS/CLAUDE/GEMINI/CI；冲突生成候选文件（如 `HARNESS.harness-new.md`）
  或最小合并；已存在违规列入历史债 baseline，**只拦新增**。判据见 protocol「旧项目执行口径」。

## 多工具入口（机制 0）
`AGENTS.md` 是唯一真契约。对不原生读它的工具放**薄指针**：Claude Code → `CLAUDE.md`、
Gemini CLI / Antigravity → `GEMINI.md`，内容只有一行 `@AGENTS.md` 导入。**指针只指，不写规则**。

## 资源
- `templates/` — 拷到目标项目根目录，`*.template.md` 去掉 `.template`，替换 `<PROJECT>`/`<MISSION>` 等占位符
- `reference/AI-ADOPTION-PROTOCOL.md` — 完整执行协议 + 给 AI 的固定指令 + 输出格式（**必读**）
- `reference/INSTANTIATION-CHECKLIST.md` — 逐条勾的落地清单
- `reference/METHODOLOGY.md` — 11 个机制为什么存在、如何按项目规模裁剪
- `reference/HARNESS-ENGINEERING.md` — Guides / Sensors / Self-correction / Steering 上位模型与边界
- `examples/node-orders-api/` — 异构完整样例（红线 grep 守门已验证可拦违规），照着看「填成什么样」

## 最关键的一条
机制 2.5（红线守门）不可跳过——**红线没有机械闸门就只是装饰**，制造「我们有规矩」的假象比没规矩更危险。
红线的黄金标准：**能写成一行 grep / lint 命令**。写不出命令的不是红线，降级到北极星原则或普通规范。

但写不出机械命令不代表不重要：语义与权衡登记为 Inferential Review Criterion，业务意图、风险和责任登记为 Human Acceptance Decision。关键 Behaviour 必须有独立证据，当前实现 agent 自生成的测试不能成为唯一验收依据。
