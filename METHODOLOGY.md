# 方法论 —— 为什么这套 Harness 这么设计

> 作者：Bryant Yang
>
> 本文解释 11 个机制各自**解决什么问题、什么时候该裁剪**。读完你就能判断哪些该原样搬、哪些该砍。

---

## 总纲：文档即契约（Docs-as-Contract）

传统项目的「规矩」活在三个地方：人脑、聊天记录、code review 时临时拍。三者都会漂移，且对 AI agent 完全不可见——每个新会话都要重新解释项目。

这套框架的赌注是：**把约束写成可索引、可 grep、可驳回的文档，让它成为唯一事实源**。判据有三：

- **可索引**：agent 进场能在 30 秒内定位「我这个任务该读哪份」。
- **可 grep**：红线能用一行命令自查（`import 'cesium'` / `as any` / `ht.cesium`）。
- **可驳回**：违反不是「讨论一下」，而是直接 reject，没有例外讨论的空间。

2.0 在这三个判据之上增加第四个：

- **可闭环**：重要目标在行动前有 Guide，行动后有 Sensor；反馈能让 agent 自修，重复失败或高严重度逃逸能进入 Experience Promotion，由 Owner 决定是否晋级。

2.2 再补两个不增加日常步骤的判据：

- **可路由**：上下文按 always-on / task-loaded / phase-loaded 分层，任务入口能证明关键事实没有漏载；
- **可学习**：失败先修当前任务，稳定经验先成为可评测 Candidate，未经 Owner 批准不自动改写正式 Skill 或契约。

## 上位模型：Direction + Context + Guides + Sensors + Experience

Harness Framework 建设的是 coding agent 的**用户侧 outer harness**，不是模型或 agent 产品内部的 system prompt、检索与编排。单个 `AGENTS.md`、Skill、lint 或 CI 都只是控制元件，完整 Harness 必须形成闭环：

```text
Guide → Agent 变更 → Sensor → Self-correction → 再验证
  ↑                                             │
  └── Evidence → Candidate → Eval → Owner → 升级控制 ─┘
```

四个维度用于审计 Harness 的覆盖与错配，不要求每条控制填写完整矩阵：

| 维度 | 分类 |
| --- | --- |
| 方向 | Feedforward Guide / Feedback Sensor |
| 执行 | Computational / Inferential / Human |
| 目标 | Maintainability / Architecture Fitness / Behaviour |
| 时机 | 本地 / 提交门禁 / 人工 Review / 集成后 / 持续健康 / 运行时 |

三条边界必须同时守住：

1. **能计算的不要推理**：类型、依赖、格式、覆盖率等交给确定性工具。
2. **无法形式化的不伪装成红线**：语义与权衡进入 inferential review criterion。
3. **业务意图不让 agent 自签**：关键 Behaviour 保留独立证据和 Human acceptance。

完整论述见 [`docs/HARNESS-ENGINEERING.md`](docs/HARNESS-ENGINEERING.md)。

---

## 机制 0 + 1 —— 多工具入口指针 + 唯一契约源

**问题**：这套框架的读者是 agent,不是人。而各家工具自动发现的入口文件名不同——Claude Code 读 `CLAUDE.md`、Gemini CLI 读 `GEMINI.md`、Codex/Cursor/Copilot/Windsurf 读 `AGENTS.md`、反重力 Antigravity 优先读 `GEMINI.md`。如果每个文件各写一份规则,必然漂移。

**做法（两个机制是一体两面）**：

- **机制 1 唯一契约源**：`AGENTS.md` 是**唯一项目入口**；具体规则分别由指定 Owner Doc 持有。它正好是 [agents.md 开放标准](https://agents.md/)(Linux 基金会 Agentic AI Foundation 主推),20+ 工具原生读取,所以「单一源」这个选择同时拿到了「最大兼容」。
- **机制 0 入口指针**：对**不**原生读 `AGENTS.md` 的工具(Claude Code、Gemini CLI),放一个**薄指针文件**,内容只有「契约源是 AGENTS.md,先读它」+ 一行 `@AGENTS.md` 导入。对优先级会盖过 AGENTS.md 的工具(Antigravity 的 `GEMINI.md`),也放薄指针,避免「空文件覆盖真契约」。

**铁律**：**指针只指,不写规则**。任何指针文件里冒出一条实质约束,就是漂移的起点,搬回对应 Owner Doc，由 `AGENTS.md` 路由。

**为什么不直接每个工具写满**：N 份满配置 = N 处要同步,改一条红线要改 N 个文件,迟早不一致。一份真契约 + N 个指针 = 改一处,处处生效。

**裁剪**：机制 1 不可裁。机制 0 按你团队实际用的工具放对应指针——只用 Codex/Cursor 的话一个指针都不用放(它们原生读 AGENTS.md);团队里有人用 Claude Code、有人用 Gemini CLI,就放对应那两个。各家支持随版本变化,落地前核对当时文档。

---

## 机制 2 —— 工程契约：方向 + 北极星 + 红线

`HARNESS.md` 是写代码、改架构、合 PR 的钢印。它有三个不可替代的部分：

**Direction Contract**：在现有 §0.0 内回答当前基线、目标状态、不变量 / 非目标、关闭证据引用和谁有权改方向。它不是新增计划文档，也不要求引入 Attractor 术语；只是避免“任务完成”退化为 executor 自报。

**北极星原则**（5–7 条）：项目级价值排序。例如「单一来源」「边界先行」「可测胜过可看」「反 God-Class」。当两个做法冲突时，用北极星裁决，而不是各凭口味。

**红线 N 条**：驳回级硬约束，**稳定编号、机械检测、违反阻断**。红线和「最佳实践」的区别在于——最佳实践是建议，红线是「碰了就 reject，不讨论例外」。

> 红线的黄金标准：可稳定机械判断且有合法 / 违规 / 错误探针。grep 仅提供文本 smoke，语法 / 语义约束需要 AST / lint / 结构测试；需要权衡的判断登记为 review criterion。

**裁剪**：Direction Contract 与北极星必留，但小项目各写一两行即可。红线按项目实情，宁少勿滥——10 条真红线 > 30 条没人查的「红线」。

### 机制 2.5 —— 红线的牙齿（enforcement，决定 harness 有效还是摆设）

> 这是从 dw_gis3d 实践里反推出来、最容易被漏掉、却最决定成败的一层。

**问题**：红线写进 `HARNESS.md §8` 只是**声明**。如果没有任何东西在查它，agent 在长会话里会漂移、会「就这一次」破例，红线就退化成装饰。「我们有规矩」的假象比没规矩更危险。

**做法**：每条红线**必须**编译成一道机械闸门，三选一（或叠加）：

- **grep 闸门**（`scripts/check-redlines.sh`）：最跨语言。「禁止出现 X」类红线一行 grep 搞定，命中即 `exit 1`。
- **lint 规则**（`no-restricted-imports` regex / `no-explicit-any`）：「禁止 import」「禁止类型逃逸」「单向依赖」编译成 lint error。
- **commitlint / CI 阈值**：提交格式、覆盖率这类。

最后由 **CI + branch protection** 兜底：闸门不全绿，**agent 想合也合不进**。这是启用的阻断红线可执行的基础；Legacy 对已批准 baseline 只拦新增违规。

**黄金判据**：红线 ⇄ 守门命令**一一对应**。`HARNESS §8` 用三列表（红线 \| 守门命令 \| 谁拦）强制你为每条红线填出那行命令。**填不出命令的不是红线**——降级到北极星或普通规范，别让查不了的东西冒充红线。

**为什么 dw_gis3d 的 harness 有效**：它的 R6/R13（禁 cesium/HT 引用）不是靠人记，是被 `eslint.config.ts` 的 regex 挡死的——违反就过不了 `pnpm lint`，CI 直接拦。把这层抽掉，那套 HARNESS.md 就只是一篇漂亮的文档。

**跨语言**：契约是「每条红线必须有机械守门命令」，**工具是实现细节**——换实现、不换契约。文档层 + grep 层（`check-redlines.sh`）+ commitlint + CI 骨架**跨语言免费**（约 80%）；只有「禁 import / 单向分层」类红线的自动闸门要换成目标语言等价物（约 20%）：

| 红线类型 | TS | Java | Python |
| --- | --- | --- | --- |
| 禁 import / 单向分层 | eslint `no-restricted-imports` | ArchUnit / Checkstyle / maven-enforcer | import-linter / flake8-tidy-imports |
| 禁类型逃逸 | eslint `no-explicit-any` | Error Prone / SpotBugs | ruff / mypy `disallow_any` |
| 通用「禁止出现 X」 | `check-redlines.sh`（改后缀，零逻辑改动） | 同左 | 同左 |
| commit 格式 / CI 兜底 | commitlint / Actions | commitlint / `mvn verify` | commitlint / `ruff`·`pytest` |

`enforcement/` 已按语言出骨架（`ts/` `java/` `python/`），拷对应子目录填占位符即可，不必从零接。所以跨语言是「换实现的有限工作」，不是重写。

**裁剪**：每条启用的机械红线必须有闸门；没有这类风险时可标记不适用，不为满足数量编造规则。观察模式与待实现控制单列。

---

## 机制 3 —— 业务规格总纲（SPEC）

**问题**：业务、产品、开发对「系统该做什么」理解不一致，到联调才发现。

**做法**：`docs/SPEC.md` 是共同语言。三个关键设计：

- **用例编号** `UC-<模块>-<序号>`：PR 描述里引用编号，可追溯。
- **固定基础模板**（角色/触发、前置、数据契约、主流程、异常分支、涉及消息、验收）：强制把「异常分支」「可测验收」写出来，而不是只写 happy path。关键 Behaviour 再追加独立证据来源与人工验收边界。
- **阶段一览**：用例挂到里程碑，避免无序开发。

**裁剪**：纯工程库/工具可以砍掉 SPEC，只留 HARNESS。有真实业务方的产品必留。

---

## 机制 4 —— 场景化工作流表 + Context Routing ★ 框架的核心齿轮

**问题**：契约写得再全，agent 不知道「我这个任务该看哪几页」，要么全读（烧上下文）要么瞎猜。

**做法**：`docs/workflow.md` §1 是一张表，把任务分成 N 种典型场景，每行回答 5 个问题：

| 场景 | 先读哪份 | 必守红线 | 产出落在哪 | DoD |

agent 进场第一动作就是「在这张表里定位我属于哪一行」。配套的 Context Routing Contract 把上下文分成三层：

- **always-on**：稳定入口、当前方向、全局红线；
- **task-loaded**：命中场景后才加载的 SPEC、模块契约和相关 ADR；
- **phase-loaded**：只在 commit、release、迁移或外部副作用阶段加载的规范与批准条件。

路由本身也要可验证。Routing Probe 至少检查：场景是否命中、任务涉及的路径 / 边界是否有 Owner Doc、关闭证据锚点是否可达。在平台规则与用户当前指令之下，项目事实 / Owner Doc > Skills > memory / 建议性上下文。若来源冲突，停止该分支并暴露冲突，不让 agent 平均融合。

**裁剪**：不可裁。这是把「一堆契约文档」变成「可操作流程」的关键转换器。小项目可以只有三行场景和一句 Probe，不需要额外路由器或运行时。

---

## 机制 5 —— ADR 决策记录

**问题**：半年后有人问「为啥用 X 不用 Y」，没人记得，于是推翻重来。

**做法**：每个重大工程决定写一篇 `docs/adr/NNNN-<title>.md`。三条铁律：

- **不可变**：ADR 合入后只能用新 ADR（标 `Supersedes`）修订，不准编辑旧的。历史是档案，不是草稿。
- **必含回滚条件**：什么信号出现时该推翻这个决定。
- **何时写有明确触发**：引入/剔除依赖、改跨模块约定、调性能预算、做红线例外、「未来 6 个月有人会问为啥」。

**裁剪**：有重大决策时采用 ADR；小工具无需空档案。Accepted 历史不变，当前 HARNESS 必须更新；替代关系只在明确决策领域生效。

---

## 机制 6 —— 业务决议卡（Decision Cards）

**问题**：ADR 回答「工程上怎么做」，但「系统业务上该做什么」的待决问题是另一类——它们该由业务方拍板，且**没拍板前不该启动对应开发**。

**做法**：`docs/decisions/` 维护 Q-NN 卡片状态（⏳ 待决 / ✅ 已决 / 🔁 重审）。关键设计：**⏳ 状态阻断对应里程碑启动**——把「需求没定就别写」变成可见的闸门。

**与 ADR 的关系**：业务决议（Q-NN，「做什么」）可能触发一篇 ADR（「怎么做」）；反向 ADR 不能独自改写业务事实。

**裁剪**：业务边界清晰的项目可砍。需求频繁悬而未决的项目，这是止血点。

---

## 机制 7 —— 提交规范

Conventional Commits（`type(scope): subject` + body 解释 why），CI commitlint 强制。核心约束：

- **body 解释 why，不复述 what**——代码本身说 what。
- `git add` 显式列文件，禁止 `git add .`／`-A`——杜绝误提交。
- 禁止 `--no-verify`／`--no-gpg-sign`。

**裁剪**：type/scope 列表按项目改，格式本身别动（生态工具依赖它）。

---

## 机制 8 —— 文档地图（按角色）

`README.md` 用一张「你是谁/你要做什么 → 直接读哪份」的表，做全套文档的总入口。避免新人/agent 在十几份 md 里迷路。

**裁剪**：文档超过 5 份就值得有。

---

## 机制 9 —— 提交前自查清单

合入前自问、适用项通过才能完成验收：用例编号写了吗？DoD 勾了吗？启用控制通过且已批准 baseline 无新增违规了吗？CI 全绿吗？该起的 ADR 起了吗？commit 合规吗？相关 Sensor 复验了吗？关键 Behaviour 有独立证据或明确的人类验收吗？

**裁剪**：只核对适用项，必要检查失败或未运行不能说完成；删去未采用的 SPEC / 里程碑 / ADR 引用。

---

## 机制 10 —— Control Map + Experience Promotion

**问题**：原有红线三列表能证明硬门禁有牙齿，但仍回答不了四件事：软约束由谁 review、关键行为靠什么独立证据验收、同类错误重复发生后谁升级 Harness、稳定工程经验如何长成 Skill 而不堆积噪声。

**做法**：实例化 [`templates/docs/harness-controls.template.md`](templates/docs/harness-controls.template.md)，维护三组轻量记录和一组引用：

- **覆盖边界**：Maintainability、Architecture Fitness、Behaviour 各自覆盖到哪里，明确不保证什么。
- **Control Map**：最小只填目标 → Guide → Sensor / 人工确认 → 失败处置 → Owner；类型、目标类别和生命周期仅在审计发现歧义时追加。
- **Behaviour Evidence 引用**：证据唯一写在 `SPEC.md`，Controls 只保存用例锚点与相关 Control，避免双写。
- **Experience Promotion**：同类失败至少两次，或一次高严重度逃逸，才创建 Evidence Packet 与 Candidate；初始化时不建空台账。

Experience Promotion Loop 是：

```text
失败 / 人工纠正 / 审计漏检
→ 修复当前任务
→ 重复或高严重度逃逸
→ Evidence Packet
→ 分类并创建 Candidate
→ 原失败回放 + 反例 / 非适用例 + 路由 smoke
→ Owner 批准
→ 发布、观察、必要时回滚
```

分类决定经验落点，避免所有问题都长成 Skill：

| 经验性质 | 正式落点 |
| --- | --- |
| 项目事实 / 业务决定 | SPEC、ADR 或对应 Owner Doc |
| 跨任务可复用的工作方法 | Candidate Skill |
| 可稳定机械拒绝的模式 | Redline / Gate |
| 语义审计漏检 | Sensor / review rubric |
| 重试、状态、幂等、确定性转换 | 普通代码 |
| 一次性上下文 | task note / memory，不晋级 |

Candidate 必须记录纠正证据或 diff、适用与不适用范围、触发条件、正反例、目标输出、Owner、版本和回滚条件。自主提炼的经验先成为 Candidate，不自动覆盖正式控制；用户明确授权维护某个 Skill / 契约时直接修改并验证。召回、评测与退役见 [`docs/experience-learning.md`](docs/experience-learning.md)。

约束分三级，不把所有重要事情都硬塞进 grep：

1. `Deterministic Gate`：能稳定机械判断，违反必拦。
2. `Inferential Review Criterion`：需要语义与权衡，输出证据和建议。
3. `Human Acceptance Decision`：涉及业务意图、风险和责任，由明确责任人签收。

**裁剪**：小项目按实际风险保留必要 Control Map 行和一段覆盖边界；可以裁行数，不能裁“重要目标必须有检测或人工确认路径”这个原则。

### 实例化后的增量维护

首次接入完成后，普通 Harness 变更不应重跑完整实例化。维护只沿受影响的闭环传播：修改 Redline / Gate、Guide、Sensor、SPEC Behaviour 或 AI-facing 入口时，同步它的唯一事实源、必要引用与配套控制，并复验受影响的 Sensor；Gate 变更还要补一次负向校准。具体影响矩阵见 [`AI-ADOPTION-PROTOCOL.md`](AI-ADOPTION-PROTOCOL.md) 的“已接入项目维护口径”。

普通业务改动、单次普通 Sensor 触发后只修正当前任务的业务实现、只读审计，不自动进入这条维护路径；修改 Sensor 本身仍需按影响维护。重复失败或高严重度逃逸才进入 Candidate-first 晋级。

### 可选 Runner Consumption Contract

只有项目实际存在 Codex Goal、Mission Driver 或其他长期 runner 时，才在 controls 中补一段消费契约，不创建新的强制顶层文件：

- 输入：目标 / 范围 / 非目标、Guides、Sensors、关闭证据、预算、权限、人工批准和停止 / 升级条件；
- 输出：当前状态、证据、失败 Sensor、下一动作、外部副作用与审计记录；
- 边界：runner 不拥有项目事实，不得静默降低控制，不能以 executor 自报替代关闭证据。

Harness Framework 只定义该边界，不实现 flow DSL、恢复引擎或任务编排平台。

---

## 怎么裁剪：按项目规模

| 规模 | 建议取哪些机制 |
| --- | --- |
| 个人脚本 / 小工具 | minimal：AGENTS + HARNESS + workflow + Controls；机械红线按实际风险启用 |
| 单人/小队产品 | product：minimal + SPEC / Behaviour Owner Doc；commit / ADR 按实际路径增加 |
| 多人 + 真实业务方 | 全部 11 个，Behaviour evidence 不可省 |
| 替换型 / 强约束迁移项目 | 全部 11 个，且红线要写「禁止旧依赖复活」并维护 baseline |

> 原则：**机制是用来减少漂移的，不是用来摆样子的。** 没人查的契约比没有契约更糟——它制造「我们有规矩」的假象。每加一条红线、一个场景、一张卡，都要能回答「谁来查、怎么查」。
