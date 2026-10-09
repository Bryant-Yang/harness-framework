# AI 自动接入与增量维护协议

<!-- harness:maintenance-routing=delta-impact -->
<!-- harness:ai-assets-audit=conditional -->
<!-- harness:context-routing=progressive-and-probed -->
<!-- harness:experience-promotion=candidate-first -->
<!-- harness:runner-consumption=optional -->

> 作者：Bryant Yang
>
> 本文把 harness 的首次接入与后续维护固化成 AI 可执行协议。新旧项目首次接入时执行：
> **审计事实与 Harnessability → 冻结 Direction / Context Routing → 实例化文档 → 建 Control Map → 生成红线 → 接 enforcement → 负向验证与自修 → 在 SPEC 补行为证据 → 按触发条件输出 Experience Candidate 与未决项**。已接入项目只按变更影响做增量维护。

## 适用场景

- 新项目：从空仓库或早期骨架开始，把 harness 一次性铺好。
- 旧项目：已有代码、README、CI、约定和历史债，把 harness 接进去但不破坏现状。
- 迁移 / 替换项目：需要禁止旧依赖复活，且希望 AI 每次进场都能守住边界。
- 已接入项目维护：已经完成 Harness 实例化，只维护受影响的 Redline、Guide、Sensor、Behaviour 或 AI-facing 入口。

## 适用边界与授权

本协议针对用户已授权的项目 Harness 接入和维护。普通业务修改或本机 Agent 规则维护不触发项目全套实例化。已有接入只改受影响部分；新接入按真实风险选择必要文件与控制，不为模板数量补规则。文中的 Candidate → Eval → Owner 针对从其他任务中自主提出的经验晋级；用户已明确要求维护某份 Skill / 契约时，该范围内按授权直接修改并验证，不重复索取相同批准。真实共享契约变更、发布及外部操作仍核对各自权限。

## 核心原则

1. AI 负责判断与填空：审计现状、识别分层、抽取风险、写出红线候选。
2. 脚本负责确定性动作：复制模板、替换占位符、grep 红线、跑验证。
3. CI 负责最终兜底：违反红线时合不进主分支。
4. 旧项目不暴力覆盖：已有文档先保留，冲突时生成候选版本或合并。
5. 红线必须可执行：写不出 grep / lint / CI 守门的，不准叫红线。
6. 重要目标必须闭环：行动前有 Guide，行动后有 Sensor 或明确的人类确认路径。
7. 约束分级：确定性 Gate、推理型 Review Criterion、人类 Acceptance Decision 不混用。
8. 行为证据独立：当前实现 agent 自己生成的测试不能成为关键行为的唯一验收依据。
9. 维护按影响传播：已接入项目不重跑完整实例化，只同步受影响的事实源、引用和控制，并做最小复验。
10. 上下文渐进加载：稳定入口不变，按 always-on / task-loaded / phase-loaded 路由，并用 Routing Probe 检查漏载与冲突。
11. 经验先候选后晋级：单次普通失败先修当前任务并在既有记录留类别和证据；重复独立同根因事件至少两次或严重逃逸才建 Candidate。按经验协议召回、评测、晋级或退役，已有明确维护授权不重复审批。
12. Runner 只是可选消费者：仅在项目实际存在时补 Consumption Contract，不把本框架扩成运行时平台。

## 首次接入统一流水线

```text
1. Project Audit + Direction
   识别技术栈、目录结构、构建/测试/lint/CI、现有 agent 配置、类型反馈、模块边界、
   测试隔离性、运行日志和关键行为证据；若实际存在 Agent 定义、Skills、编排器或工具专用规则，
   再核对声明与文件、悬空引用、职责重叠和复用机会。在 HARNESS §0.0 记录当前基线、目标状态、
   不变量 / 非目标、Closure Evidence 与 Change Authority。

2. Context Routing + Harness Instantiation
   定义 always-on / task-loaded / phase-loaded 与 Routing Probe；
   生成或合并 AGENTS.md、HARNESS.md、docs/workflow.md、docs/harness-controls.md、
   commit 规范和必要指针文件，并记录框架版本与本地差异。

3. Control Mapping
   把重要目标最小映射为 Guide、Sensor / 人工确认、失败处置和 Owner；
   用覆盖边界审计 Maintainability / Architecture Fitness / Behaviour，只对疑难 Control 追加类型与生命周期注记；
   对实际存在且高影响的系统边界，Sensor 验证 producer 实际输出 → contract / transform → consumer 真实预期。

4. Redline Design
   从真实风险提炼必要的可机械检查红线，不设最低条数，并登记到 HARNESS §8；没有此类风险时明确不适用。

5. Enforcement Wiring
   为每条红线接 grep / lint / commitlint / CI 守门。

6. Negative Verification + Self-correction
   故意写一条违规探针，确认守门失败且反馈足以指导修复；删除探针，再确认守门通过。

7. Behaviour Evidence
   在 SPEC 对关键用例登记独立证据、批准人和人工边界；Controls 只引用用例，不双写证据。

8. Handoff + Experience Promotion
   输出已接好的控制、红线、覆盖边界、历史债 baseline 和人工待决；只有同类失败至少两次、
   已有趋势证据或一次高严重度逃逸时才输出 Candidate。自主 Candidate 必须分类、评测并有对应 Owner 授权后晋级；已有明确维护授权不重复批准。
```

## 现有 AI-facing 资产审计（条件式）

只在项目实际存在 Agent 定义、Skills、编排器或工具专用规则时执行；没有这些资产时跳过，不创建空清单或永久资产台账。

1. 枚举实际文件和入口声明，逐个解析它们引用的文件、命令、发现方式、触发条件与职责。
2. 悬空引用和缺失目标属于确定性问题；在当前任务授权范围内修复，超出范围则只报告，不借审计扩大改动。
3. 内容完全相同或职责相近只是审计证据。必须结合消费者、自动发现入口、触发条件、职责和兼容需求判断；不同工具各自必需的薄指针不算重复资产，也不得仅凭内容相同自动删除。
4. 对现有资产之间或新增资产与现有资产按以下顺序分类：现有资产已完整覆盖（包括可发现性与触发覆盖）、可泛化后复用、意图明确的专业化分工、职责不同。
5. 只有确认同一入口 / 触发、同一职责且没有独立兼容需求时，才建议复用或合并；“语义相近”是推理型判断，必须给出证据，不能伪装成 Gate。
6. 审计结论写进当前变更说明或 review，不要求目标项目长期维护另一份资产目录。

## 新项目执行口径

新项目按已授权目标和真实风险选择最小闭合组合，见 [`docs/instantiation-profiles.md`](docs/instantiation-profiles.md)：

- 仅复制所选组合需要的模板；ADR、提交规范、SPEC 和工具指针按实际用途增加。
- `*.template.md` 去掉 `.template`。
- 将框架版本与来源 commit 记录到 `docs/harness-controls.md`。
- 填入项目事实和日期；作者仅在项目要求或决策责任需要时填写，不在代码中普遍加署名。
- 红线数量由真实风险决定；语义与权衡采用 review criterion，不为凑数量制造 Gate。
- 对每条启用的红线接机械守门，并按实际提交/集成路径接入现有 CI；外部设置变更须有对应权限。
- 有关键业务行为时，在 SPEC 或已确认的 Behaviour Owner Doc 登记独立证据；纯工具项目在覆盖边界注明业务验收不适用，仍验证工具的公开行为。

完成标准：

- `AGENTS.md` 是唯一项目入口；工程、业务、提交等事实分别由指定 Owner Doc 持有，入口只路由，不复制规则。
- 所有启用的 `HARNESS.md §8` 红线都有可执行守门；无机械红线时写明风险判断与适用的其他控制。
- `docs/harness-controls.md` 里的重要目标都有 Sensor 或明确的人类确认路径。
- workflow 已区分 always-on / task-loaded / phase-loaded，Routing Probe 能发现漏载的 Owner Doc 或 Closure Evidence。
- 实际启用的 Sensors 能通过；确定性控制的相关负向探针被拦住、清理后恢复通过。
- 实例化文档闭合：无已知框架占位符、未改名模板或悬空本地引用，所选组合能通过实例化检查。

## 旧项目执行口径

旧项目先审计，再接入：

- 不覆盖已有 `README.md`、`AGENTS.md`、`CLAUDE.md`、`GEMINI.md`、CI 配置；禁止将全部模板直接复制或重命名覆盖目标文件。
- 冲突时生成候选文件，如 `HARNESS.harness-new.md`，或在原文件中最小合并。
- 已存在违规先列为历史债，不直接要求全仓清零。
- 新增违规必须从接入当天开始被拦。
- baseline 必须有生成方式和 diff 方式，不能只写一句“历史债以后处理”。
- 红线优先选择最容易失控的边界：旧依赖复活、跨层 import、裸配置、类型逃逸、绕过封装层。

完成标准：

- AI 能在 `docs/workflow.md` 里定位常见任务场景。
- 历史债有清单，不和新增违规混在一起。
- 所有启用的阻断红线均有机械守门；待实现或观察模式的候选控制单列，不能宣称已守门。
- 历史违规保留在已批准 baseline，后续 PR 不能新增违规或静默扩大 baseline；验收检查新增差异，不要求历史命中全部清零。
- Control Map 明确哪些是观察模式、哪些是阻断模式，并有逐步收紧计划。

## 迁移 / 替换项目额外要求

迁移型项目若目标包含删除旧依赖，必须为禁止旧依赖复活建立控制；编号按现有项目保持稳定，不强制重新编号：

```text
R<项目编号> 在已批准入口范围禁止旧依赖引用
守门：grep / lint 禁 import <legacy>、@<legacy-scope>、window.<legacy>
```

grep / 静态 import lint 只覆盖有限文本或语法子集。声明更强保证前列清实际入口（静态、动态、运行时依赖），为每个入口接相应检查及正负探针，未覆盖部分明确记录。

如果旧依赖历史上仍存在：

- 先生成 baseline 清单。
- 禁止所有新增引用，包括已有文件的新命中；不能只检查新增文件。
- 每清掉一批历史引用，就收紧 baseline。

## 已接入项目维护口径

仅当项目已经完成 Harness 实例化，且当前任务修改 Harness、控制、AI-facing 资产或框架版本时进入本节。普通业务改动、单次普通 Sensor 触发后只修正当前任务的业务实现、只读审计、尚未达到 Experience Promotion 条件的失败都不触发 Harness 维护；修改 Sensor 本身仍进入下表。

| 变更对象 | 必须同步 | 最小复验 | 明确跳过 |
| --- | --- | --- | --- |
| Redline | `HARNESS.md §8`；workflow 编号引用；enforcement；Control；涉及的 baseline | 正向通过 + 目标负向探针失败并清理；baseline 不扩大 | 无关红线与全量重新实例化 |
| Guide | Guide 唯一事实源；workflow / Control 引用；配对 Sensor；高影响项的 Owner | 链接可达 + 配对 Sensor 可执行或人工责任明确 | 纯措辞扩写与全量文档重写 |
| Sensor / 非红线 Gate | 检查、review criterion 或人工协议的唯一事实源；Control；运行时机、失败反馈与修复方向 | 确定性项做正负验证；推理项保留证据；人工项确认验收责任 | 因为可机械执行就抬成 Redline，或为凑门禁而降低阈值 |
| SPEC Behaviour / Evidence | `SPEC.md` 唯一事实源；相关数据契约、tests / fixtures；Control 锚点与人工边界 | 独立证据、验收责任和引用锚点仍成立 | 在 Controls 复制证据正文 |
| AI-facing 入口 / Skill / Agent | 实际资产自身持有职责与触发条件；仅当项目级契约或路由受影响时同步 `AGENTS.md`；工具入口只保留引用 | 结构与引用检查 + 最小 smoke；工具入口保持薄指针 | 集中登记全部资产，或仅因 `AGENTS.md` 内容变化就向各指针复制规则 |
| Context Routing | workflow / AGENTS 的层级、Owner Doc 优先级与 Probe；只同步受影响场景 | 场景命中 + 路径 / 边界 + Closure Evidence 路由 smoke | 全量加载所有文档或新建重型路由服务 |
| Experience Candidate | Evidence Packet、分类、适用 / 不适用、触发与正反例、Owner、版本 / 回滚 | 原失败回放 + 反例 / 非适用例 + 路由 smoke + 独立评测 | 自动覆盖正式 Skill / Guide / Sensor / Gate |
| Runner Consumption（仅存在时） | runner 输入 / 输出、权限、预算、人工批准、停止条件与 Closure Evidence | 最小执行 / 恢复 smoke + 外部副作用审计 | 为不存在的 runner 建空配置，或让 runner 拥有项目事实 / 弱化门禁 |

框架上游升级继续使用 `docs/harness-controls.md` 中记录的版本、本地差异和人工审查策略；不另建维护日志。维护完成时只报告本次变更对象、同步面、最小复验和明确跳过的无关步骤。

## 给 AI 的固定指令

把下面这段交给 AI，即可让它自动接入 harness：

```text
请把 harness 框架落到当前项目。

要求：
0. 先判定执行模式：
   - 若项目已经完成 Harness 实例化，且本次是维护任务，转到“已接入项目维护口径”
   - 只审计矩阵中受影响的事实；仅当变更涉及 AI-facing 资产时，才审计这些资产
   - 不继续执行首次接入的 1-8 全量步骤，只执行受影响的同步与复验，然后使用“增量维护”输出格式
   - 若属于首次接入，再继续下面的完整流程

1. 首次接入时审计当前项目事实：
   - 技术栈
   - 目录结构
   - 构建 / 测试 / lint 命令
   - 现有 README / AGENTS / CLAUDE / GEMINI / CI 配置
   - 仅当实际存在时，审计 Agent 定义 / Skills / 编排器 / 工具专用规则，核对引用有效性、职责重叠与复用机会
   - 已存在的架构约束和常见风险
   - Harnessability：类型反馈、模块边界、测试隔离性、运行日志、关键行为证据
   - 在 HARNESS §0.0 写清当前基线、目标状态、不变量 / 非目标、Closure Evidence 与 Change Authority

2. 首次接入时从 harness templates 实例化；增量维护跳过本步：
   - 按 docs/instantiation-profiles.md 选择闭合组合，仅生成必要文件
   - AGENTS.md 入口、HARNESS.md 方向/工程事实、docs/workflow.md 路由、docs/harness-controls.md 控制
   - SPEC、ADR、提交规范按实际业务/决策/提交路径增加；已有 Owner Doc 可保留并在入口明确绑定
   - 必要的 CLAUDE.md / GEMINI.md / .github/copilot-instructions.md / .cursor/rules 指针
   - 存在启用的机械红线时，生成或复用对应守门脚本
   - 在 AGENTS / workflow 定义 always-on / task-loaded / phase-loaded；Routing Probe 检查场景、改动路径 / 边界和 Closure Evidence
   - 在平台规则与用户当前指令之下，项目事实 / Owner Doc > Skills > memory / 建议性上下文，冲突时显式报告

3. 建立 Control Map：
   - 每个重要目标最小登记 Guide、Sensor / 人工确认、失败处置和 Owner
   - 只有执行方式、信任边界或成本不清时，才追加 Guide/Sensor 类型、目标类别和生命周期
   - 区分 Deterministic Gate / Inferential Review Criterion / Human Acceptance Decision
   - 明确 Maintainability / Architecture Fitness / Behaviour 的覆盖边界和不保证项
   - 仅对实际存在且高影响的系统边界，验证 producer 实际输出 → contract / transform → consumer 真实预期；不要只分别证明两端存在

4. 如果是旧项目：
   - 不全量复制模板，不覆盖已有重要文档；冲突时保留旧文件，生成候选版本或做最小合并
   - 红线只写能机械检查的，不要拍脑袋
   - 已存在违规先列为历史债，不要直接让全仓 CI 失败
   - 新增违规必须能被拦
   - baseline 要有生成和 diff 命令，按风险逐步收紧

5. 如果是新项目：
   - 按实际风险与授权范围选择模板，不生成无用途的骨架文件
   - 用项目使命、技术栈、目录规划填充占位符
   - 红线数量由真实风险决定，不为凑数新增约束

6. 对启用的机械红线，enforcement 必须接好；没有此类风险时记录不适用：
   - 每条启用的 HARNESS 红线都要有 grep / lint / CI 守门；已有历史债按 baseline 只拦新增
   - 跑项目实际守门命令（使用模板脚本时为 bash scripts/check-redlines.sh）
   - 对受影响的确定性控制做有意义的负向探针，确认目标违规失败
   - 删除本次探针，再确认守门通过
   - 报错必须能定位问题，并告诉 agent 应读哪份 Guide 或往哪个边界修

7. 行为证据必须独立：
   - 在 SPEC 或已指定的 Behaviour Owner Doc 为关键用例登记 approved fixtures / 既有 contract tests / 外部样例 / 生产回放 / 人工验收之一
   - 当前实现 agent 新生成的测试不能作为唯一验收证据
   - harness-controls 只引用 Behaviour Owner Doc 的证据锚点，不复制证据正文；不适用业务规格的项目删掉 SPEC 的强制引用

8. 首次接入最后输出：
   - 生成 / 修改了哪些文件
   - 哪些红线已经机械守门
   - 哪些规则还只是文档约束
   - 哪些历史债需要 baseline
   - 哪些地方需要人工拍板
   - 单次普通失败只修当前任务
   - 仅当同类失败至少两次、已有趋势证据或一次高严重度逃逸时，输出 Evidence Packet 与分类后的 Candidate
   - 自主提出的 Candidate 依 docs/HARNESS-ENGINEERING.md 与 docs/harness-controls.md 的评测/授权规则晋级；已有明确维护授权不重复索取批准
   - 仅当检测到 Codex Goal、Mission Driver 或其他 runner 时，补 Runner Consumption Contract；否则不建空配置
```

## 实例化检查

标准路径组合运行 `python3 <framework>/scripts/validate-instantiation.py <project-root> --profile minimal`；业务产品用 `--profile product`，旧项目可追加 `--legacy`。若保留已有 Owner Doc 路径，用 `--owner direction=路径`、`--owner workflow=路径`、`--owner controls=路径`、`--owner behaviour=路径` 绑定实际事实源。检查只证明文档结构与引用闭合，不替代项目 Sensors、路由语义或人工验收。

## AI 输出格式

### 首次接入

首次接入完成后按这个格式收口：

```text
已接入：
- <文件 / 机制>

Control Map：
- <目标>：Guide=<...>；Sensor/人工确认=<...>；处置=<...>；Owner=<...>

已机械守门：
- R1 <红线>：<命令 / lint / CI>

验证：
- <命令>：通过
- 负向探针：已确认会失败，探针已删除

历史债：
- <仅旧项目需要>

行为证据：
- <SPEC 用例锚点>：<独立证据 / 批准人 / 人工验证>

人工待决：
- <需要项目负责人拍板的问题>

Experience Candidate（仅达到触发条件时输出）：
- <Evidence / 严重度与重复次数 / 分类 / 适用与不适用 / Eval / Owner / 发布与回滚>

Runner Consumption（仅实际存在 runner 时输出）：
- <输入 / 输出 / 权限与批准 / 停止条件 / Closure Evidence / 副作用审计>
```

### 增量维护

已接入项目只汇报本次实际维护的范围；没有发生的检查和不相关的控制不列空项：

```text
已维护：
- <修改文件>

维护范围：
- 变更对象：<Redline / Guide / Sensor / Behaviour / AI-facing 资产 / Context Routing / Experience Candidate / Runner Consumption>
- 同步面：<本次实际同步的事实源、引用与控制>
- 最小复验：<实际执行的命令 / review 证据 / 人工确认>
- 明确跳过：<未重跑的全量步骤与无关控制>

人工待决（仅实际存在时输出）：
- <需要项目负责人拍板的问题>
```
