# 工作流（<PROJECT> Workflow）

> 作者：<AUTHOR>　最近更新：<YYYY-MM-DD>
>
> 本文是 <PROJECT> 的「开车手册」。每次任务开工前先翻这里：你处的场景需要先读哪份文档、必须守哪条红线、产出落在哪里、DoD 是什么。
>
> 顶层契约源仍是 [`../HARNESS.md`](../HARNESS.md) 与 [`SPEC.md`](SPEC.md)。控制闭环见 [`harness-controls.md`](harness-controls.md)。本文不复述规则，只做「按场景的索引 + 红线提醒」。

<!--
这是整套框架的核心齿轮：把「一堆契约文档」转成「可操作流程」。
场景数量按项目调（小项目 3–4 行即可）。每行必须答全 5 列。
-->

## 1. 典型场景

| # | 场景 | 先读哪份 | 必守红线（[`../HARNESS.md`](../HARNESS.md) §8） | 产出落在哪 | DoD |
| --- | --- | --- | --- | --- | --- |
| 1 | **新增 / 修改业务功能（用例级）** | [`SPEC.md`](SPEC.md) 对应用例 + 数据契约 | R<单一职责> R<命名> R<状态机> R<i18n> | 实现 + 单测 + 必要时新增用例编号 | 用例验收通过 + 关联里程碑 DoD 勾选 |
| 2 | **改动 <核心封装层>** | [`../HARNESS.md`](../HARNESS.md) §4.x | R<反应性> R<禁止裸 import> R<资源清理> | `src/<封装层>/**`，不外溢到其他层 | mount/unmount 不泄漏 + lint 守门全绿 |
| 3 | **新增 / 改动 UI 组件** | [`../HARNESS.md`](../HARNESS.md) §4.x UI 段 | R<禁多 UI 库> R<UI 不耦合重依赖> R<文案接 t()> | `src/ui/<组件>/` | 无新增 UI 依赖，主题可切，a11y 焦点可见 |
| 4 | **对接外部 / 改通信契约** | 通信契约文档 + 对应 spec | R<消息走统一信封> R<origin 白名单> | `src/<通信层>/` + 类型 + 双向映射 | 新增动作同步契约文档 + ADR + 单测 |
| 5 | **加 / 改 / 删依赖** | [`deps-and-configs.md`](deps-and-configs.md) + [`adr/README.md`](adr/README.md) | R<禁旧依赖复活> R<禁第二套库> | `package.json`（lockfile 同步）+ 新 ADR | `install --frozen-lockfile` 无漂移 + ADR Accepted |
| 6 | **写一篇 ADR** | [`adr/_template.md`](adr/_template.md) | 「决策被推翻时新建而非编辑旧 ADR 正文」 | `docs/adr/NNNN-<kebab>.md` + 同步索引 | 评审通过、状态 Accepted、HARNESS 交叉引用 |
| 7 | **PR 评审** | 改动涉及的 spec 章节 + [`../HARNESS.md`](../HARNESS.md) §8 全部红线 | 全部红线 | PR 描述含：用例编号 + 里程碑 | CI 全绿 + 相关 DoD 勾选 |
| 8 | **业务填一张决议卡** | [`SPEC.md`](SPEC.md) 决议卡正文 | （业务侧无工程红线） | 在 SPEC 卡片中签名，工程同步 [`decisions/README.md`](decisions/README.md) | 状态 ⏳ → ✅ 后对应里程碑解锁 |

## 2. 红线速记

> 详见 [`../HARNESS.md`](../HARNESS.md) §8，编号严格对齐。这里只放一行速记，方便扫。

| § | 速记 |
| --- | --- |
| R1 | <一行速记> |
| R2 | <一行速记> |
| … | … |

## 3. Context Routing Contract

> 稳定入口保持不变；不同任务和阶段只载入相关事实，减少噪声。在平台规则与用户当前指令之下，项目事实 / Owner Doc > Skills > memory / 建议性上下文。

| 层级 / 会话目的 | 必载 | 按需 |
| --- | --- | --- |
| Always-on | [`../README.md`](../README.md)、本表、HARNESS §0.0 / §8 | 无 |
| 写新业务功能 | [`SPEC.md`](SPEC.md) 对应用例 | 通信契约（若涉及消息） |
| 改 <核心封装层> | [`../HARNESS.md`](../HARNESS.md) §4.x | 对应里程碑 |
| 改 UI 组件 | [`../HARNESS.md`](../HARNESS.md) §4.x UI 段 | 术语表相关词条 |
| 加 / 改依赖 | [`deps-and-configs.md`](deps-and-configs.md) | 上一篇相关 ADR |
| 起 ADR | [`adr/_template.md`](adr/_template.md) | 相关决议卡 |
| 评审 PR | [`../HARNESS.md`](../HARNESS.md) §8 + 改动涉及 spec | 里程碑 DoD |
| 处理重复失败 / 高严重度逃逸 | [`harness-controls.md`](harness-controls.md) Experience Promotion + 失败证据 | 相关 Guide / Sensor / ADR |
| Phase-loaded：准备 commit / release | [`git-commit-conventions.md`](git-commit-conventions.md) + 对应发布条件 | 回滚 / 运维文档 |
| 新成员 D1 | [`../README.md`](../README.md)、HARNESS §0/§8 | SPEC、术语表按学习目标加载 |

Routing Probe（可由 agent 自检，不新增用户动作）：场景是否命中；改动路径 / 系统边界是否有 Owner Doc；Closure Evidence 锚点是否可达。任一缺失或来源冲突时，先暴露缺口，不猜测或平均融合。

## 4. Self-correction 与 Experience Promotion

当前变更失败时：

1. 读取 Sensor 的编号、命中位置与修复方向；
2. 回到对应 Guide，修复当前变更；
3. 重跑同一 Sensor，直到通过；
4. 不得通过忽略规则、降低阈值或删除测试制造假绿。

先在既有任务 / PR 记录保留首个失败的类别与证据链接，不新增日常日志。同类失败至少两次，或一次高严重度逃逸时：把证据索引写入 [`harness-controls.md`](harness-controls.md)，先分类为项目事实、Candidate Skill、Gate、Sensor、普通代码或一次性记忆。单次普通失败只修当前问题。对自主经验晋级，Agent 先提出 Candidate；原失败回放、反例 / 非适用例、路由 smoke、Owner 批准和回滚条件齐备后才能晋级正式控制。已有针对该 Skill / 契约的明确维护授权不重复审批。状态、召回、A/B 与退役按 controls §7。

## 5. 提交前自查

按当前任务核对适用项；不适用项说明理由：

1. 涉及业务时，实际用例 / 公开行为验收证据可达吗？
2. 已设里程碑的相关 DoD 达成了吗？
3. 启用的阻断红线通过，已批准历史 baseline 无新增违规吗？
4. CI 全绿了吗？
5. 涉及新动作 / 新依赖 / 新红线例外，我起 ADR 了吗？
6. 我的 commit message 符合 [`git-commit-conventions.md`](git-commit-conventions.md) 吗？
7. 相关 Sensor 已复验通过，关键 Behaviour 有独立证据或明确的人类验收吗？
