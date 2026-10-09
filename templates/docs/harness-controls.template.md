# <PROJECT> Harness Controls

<!-- harness:control-map=minimum -->
<!-- harness:behaviour-evidence=spec-reference-only -->
<!-- harness:experience-trigger=repeat-2-or-high-severity-1 -->
<!-- harness:context-routing=progressive-and-probed -->
<!-- harness:experience-promotion=candidate-first -->
<!-- harness:runner-consumption=optional -->

> Framework version：2.3.0　项目实例版本：<YYYY-MM-DD / commit>
>
> 本文把重要目标映射为 Guide、Sensor / 人工确认、失败处置和责任人。它不替代 `HARNESS.md`、`SPEC.md`
> 或具体工具配置，只负责证明控制闭环是否完整。

## 1. 覆盖边界

| 调节目标 | 当前覆盖 | 证据索引（不复制内容） | 明确不保证什么 |
| --- | --- | --- | --- |
| Maintainability | <成熟 / 部分 / 空白> | <lint / typecheck / tests / review> | <例如：不能可靠判断是否过度设计> |
| Architecture Fitness | <成熟 / 部分 / 空白> | <结构测试 / 性能预算 / 可观测性检查> | <例如：未覆盖生产流量下的性能> |
| Behaviour | <成熟 / 部分 / 空白> | [`SPEC.md#<关键用例锚点>`](SPEC.md#<关键用例锚点>) | <例如：AI 自生成测试不是独立需求证据> |

## 2. Control Map

> 重要目标至少有一条检测或明确的人类确认路径。最小表只记录行动所需信息；四维分类用于按需审计，不要求逐项填矩阵。

| ID | 目标 | Guide（行动前） | Sensor / 人工确认（行动后） | 失败处置 | Owner |
| --- | --- | --- | --- | --- | --- |
| C1 | <目标> | <文档 / Skill / 脚本> | <测试 / lint / review / 人工验收> | <自修 / 阻断 / 建单 / 人工裁决> | <责任人> |

仅当审计发现执行方式、信任边界或成本不清时，再为相关 Control 补充 `Guide/Sensor 类型`、`目标类别` 与 `生命周期` 注记；不要为所有行预建空列。

## 3. 约束等级

| ID | 等级 | 判据 | 允许的处置 |
| --- | --- | --- | --- |
| <R1 / C?> | Deterministic Gate | <可稳定机械判断，低误报> | 违反必拦；修复后复验 |
| <S?> | Inferential Review Criterion | <需要语义或权衡> | 报告证据和建议，不伪装成确定事实 |
| <A?> | Human Acceptance Decision | <业务意图、风险或责任> | 由明确责任人签收；agent 不代签 |

## 4. Behaviour Evidence 引用

> SPEC 或项目指定的 Behaviour Owner Doc 是唯一证据源；本文只引用。纯工具组合可删本节与 SPEC 引用，注明范围并验证公开行为。

| 用例 / 风险 | SPEC 证据位置 | 相关 Control |
| --- | --- | --- |
| <UC-...> | [`SPEC.md#<锚点>`](SPEC.md#<锚点>) | <C?> |

## 5. 反馈生命周期

| 阶段 | 预算 | 必跑 Sensors | 反馈给谁 | 失败后 |
| --- | --- | --- | --- | --- |
| Agent 本地循环 | 秒级 | <相关 lint / typecheck / tests> | 当前 agent | 修复并复验 |
| 提交门禁 | 分钟级 | <redlines / 全量 lint / 相关测试> | 提交者 | 阻断提交 |
| 人工 Review | 按风险 | <语义 / spec / 风险检查> | Reviewer | 修改或明确接受风险 |
| 集成后 | 较昂贵 | <全量测试 / mutation / 架构检查> | 维护队列 | 建单或回滚 |
| 持续健康 / 运行时 | 周期性 | <漂移 / SLO / 日志异常> | Owner | 带证据提出改进，不直接改生产 |

## 6. Context Routing Sensor

> 不建新路由器。现有 `AGENTS.md → workflow` 入口至少探测：场景命中、改动路径 / 边界的 Owner Doc、Closure Evidence 锚点。缺失或来源冲突即报告；在平台规则与用户当前指令之下，Owner Doc > Skills > memory / 建议性上下文。

## 7. Experience Promotion

> 同类失败至少两次，或一次高严重度逃逸时才建立记录；初始化时只保留触发规则，不创建空表。先修当前任务，再形成 Evidence Packet。触发后记录：纠正证据 / diff、严重度与重复次数、分类、Candidate 目标、适用 / 不适用范围、触发与正反例、原失败回放、反例 / 路由 smoke、Owner、发布 / 回滚与复查日。
>
首次普通事件在既有任务 / PR 留下 failure category 和证据链接；同根因的独立事件才计重复，重试不增加事件数。达到触发条件后才建薄索引和主题条目，记录稳定 ID、candidate / evaluated / active / retired 状态、正式事实源、授权、复查 / 回滚。按场景召回，candidate 仅供维护评测，retired 默认不载入。Skill 必须比较同条件有 / 无 Skill 的成功率、误触发、修复轮数与成本，Gate 回放不代表模型收益。规则只在一个事实源维护，条目保存证据与链接；无收益或失效时退役。框架方法详见 `docs/experience-learning.md`，实例化时按项目事实吸收，不保留指向未复制框架文件的引用。

> 分类落点：项目事实 → SPEC / ADR；复用方法 → Candidate Skill；机械可拒模式 → Gate；语义漏检 → Sensor；重试 / 状态 / 幂等 → 普通代码；一次性信息 → task note / memory。Agent 不得自动覆盖正式 Skill 或契约。用户已明确授权维护该对象时直接修改并验证，记录现有授权，不重复审批。

## 8. Runner Consumption Contract（仅检测到 runner 时实例化）

> 没有 Codex Goal、Mission Driver 或外部 runner 时删除本节，不创建空配置。存在时记录：目标 / 范围 / 非目标、Guides、Sensors、Closure Evidence、权限 / 人工批准、预算与停止条件；runner 返回状态、证据、失败 Sensor、下一动作、外部副作用与审计记录。runner 不拥有项目事实，不得弱化门禁。证据绑定输入 / 代码 / 契约版本，任一相关变更使旧证据失效；外部操作超时且结果未知时先查询实际状态或幂等键，不盲目重复副作用。

## 9. Baseline 与模板升级

- **Legacy baseline**：<已批准基线文件 / 采集命令 / 只拦新增的比较命令>。扫描器只将 exit 1 解释为无命中，exit 2+ 阻断；不得用 `|| true` 吞错。框架提供 `scripts/check-baseline.py capture <baseline> -- rg -n --no-heading --color never '<模式>' src` 和 `check <baseline> -- <同一扫描命令>`；项目可复制该脚本或复用现有等价工具。按文件与内容保留重复计数，忽略行号移动；同一文件新增同样命中仍拦截。baseline 不可静默扩大，扫描输入 / 匹配策略变化须重新审查。此文本 Gate 不证明 AST / 语义覆盖。
- **模板来源**：Harness Framework `2.3.0`，来源 commit `<sha>`。
- **本地差异**：<哪些是项目事实，升级时不得自动覆盖>。
- **升级策略**：先看上游 diff，区分 bug fix / optional control / breaking policy，再人工合并并重跑负向验证。
