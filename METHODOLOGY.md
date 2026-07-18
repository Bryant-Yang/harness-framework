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

- **可闭环**：重要目标在行动前有 Guide，行动后有 Sensor；反馈能让 agent 自修，重复失败能进入 Human Steering。

## 上位模型：Guides + Sensors + Steering

Harness Framework 建设的是 coding agent 的**用户侧 outer harness**，不是模型或 agent 产品内部的 system prompt、检索与编排。单个 `AGENTS.md`、Skill、lint 或 CI 都只是控制元件，完整 Harness 必须形成闭环：

```text
Guide → Agent 变更 → Sensor → Self-correction → 再验证
  ↑                                             │
  └──── Human Steering：观察重复失败并升级控制 ─────┘
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

- **机制 1 唯一契约源**：`AGENTS.md` 是**唯一**真契约。它正好是 [agents.md 开放标准](https://agents.md/)(Linux 基金会 Agentic AI Foundation 主推),20+ 工具原生读取,所以「单一源」这个选择同时拿到了「最大兼容」。
- **机制 0 入口指针**：对**不**原生读 `AGENTS.md` 的工具(Claude Code、Gemini CLI),放一个**薄指针文件**,内容只有「契约源是 AGENTS.md,先读它」+ 一行 `@AGENTS.md` 导入。对优先级会盖过 AGENTS.md 的工具(Antigravity 的 `GEMINI.md`),也放薄指针,避免「空文件覆盖真契约」。

**铁律**：**指针只指,不写规则**。任何指针文件里冒出一条实质约束,就是漂移的起点,立刻搬回 `AGENTS.md`。

**为什么不直接每个工具写满**：N 份满配置 = N 处要同步,改一条红线要改 N 个文件,迟早不一致。一份真契约 + N 个指针 = 改一处,处处生效。

**裁剪**：机制 1 不可裁。机制 0 按你团队实际用的工具放对应指针——只用 Codex/Cursor 的话一个指针都不用放(它们原生读 AGENTS.md);团队里有人用 Claude Code、有人用 Gemini CLI,就放对应那两个。各家支持随版本变化,落地前核对当时文档。

---

## 机制 2 —— 工程契约：北极星 + 红线

`HARNESS.md` 是写代码、改架构、合 PR 的钢印。它有两个不可替代的部分：

**北极星原则**（5–7 条）：项目级价值排序。例如「单一来源」「边界先行」「可测胜过可看」「反 God-Class」。当两个做法冲突时，用北极星裁决，而不是各凭口味。

**红线 N 条**：驳回级硬约束，**编号、可 grep、违反必停手**。红线和「最佳实践」的区别在于——最佳实践是建议，红线是「碰了就 reject，不讨论例外」。

> 红线的黄金标准：**能写成一条 grep 命令**。
> 写不成 grep 的「红线」往往是软约束，应该降级到北极星或普通规范。

**裁剪**：北极星必留（哪怕只有 3 条）。红线按项目实情，宁少勿滥——10 条真红线 > 30 条没人查的「红线」。

### 机制 2.5 —— 红线的牙齿（enforcement，决定 harness 有效还是摆设）

> 这是从 dw_gis3d 实践里反推出来、最容易被漏掉、却最决定成败的一层。

**问题**：红线写进 `HARNESS.md §8` 只是**声明**。如果没有任何东西在查它，agent 在长会话里会漂移、会「就这一次」破例，红线就退化成装饰。「我们有规矩」的假象比没规矩更危险。

**做法**：每条红线**必须**编译成一道机械闸门，三选一（或叠加）：

- **grep 闸门**（`scripts/check-redlines.sh`）：最跨语言。「禁止出现 X」类红线一行 grep 搞定，命中即 `exit 1`。
- **lint 规则**（`no-restricted-imports` regex / `no-explicit-any`）：「禁止 import」「禁止类型逃逸」「单向依赖」编译成 lint error。
- **commitlint / CI 阈值**：提交格式、覆盖率这类。

最后由 **CI + branch protection** 兜底：闸门不全绿，**agent 想合也合不进**。这是「红线全部清零」从自觉变成事实的唯一办法。

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

**裁剪**：不可裁。这是 harness「是」还是「像」的分水岭。哪怕只有一条红线，也要给它一道闸门。

---

## 机制 3 —— 业务规格总纲（SPEC）

**问题**：业务、产品、开发对「系统该做什么」理解不一致，到联调才发现。

**做法**：`docs/SPEC.md` 是共同语言。三个关键设计：

- **用例编号** `UC-<模块>-<序号>`：PR 描述里引用编号，可追溯。
- **固定基础模板**（角色/触发、前置、数据契约、主流程、异常分支、涉及消息、验收）：强制把「异常分支」「可测验收」写出来，而不是只写 happy path。关键 Behaviour 再追加独立证据来源与人工验收边界。
- **阶段一览**：用例挂到里程碑，避免无序开发。

**裁剪**：纯工程库/工具可以砍掉 SPEC，只留 HARNESS。有真实业务方的产品必留。

---

## 机制 4 —— 场景化工作流表（workflow）★ 框架的核心齿轮

**问题**：契约写得再全，agent 不知道「我这个任务该看哪几页」，要么全读（烧上下文）要么瞎猜。

**做法**：`docs/workflow.md` §1 是一张表，把任务分成 N 种典型场景，每行回答 5 个问题：

| 场景 | 先读哪份 | 必守红线 | 产出落在哪 | DoD |

agent 进场第一动作就是「在这张表里定位我属于哪一行」。配套的「**按需载入上下文表**」进一步告诉它：这个会话只载哪几份文档，省主上下文。

**裁剪**：不可裁。这是把「一堆契约文档」变成「可操作流程」的关键转换器。场景数量按项目调（dw_gis3d 用了 8 种）。

---

## 机制 5 —— ADR 决策记录

**问题**：半年后有人问「为啥用 X 不用 Y」，没人记得，于是推翻重来。

**做法**：每个重大工程决定写一篇 `docs/adr/NNNN-<title>.md`。三条铁律：

- **不可变**：ADR 合入后只能用新 ADR（标 `Supersedes`）修订，不准编辑旧的。历史是档案，不是草稿。
- **必含回滚条件**：什么信号出现时该推翻这个决定。
- **何时写有明确触发**：引入/剔除依赖、改跨模块约定、调性能预算、做红线例外、「未来 6 个月有人会问为啥」。

**裁剪**：几乎不可裁，但启动期可只要求关键几篇 Accepted。

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

合入前自问、全「是」才能 request review：用例编号写了吗？DoD 勾了吗？红线 grep 清零了吗？CI 全绿吗？该起的 ADR 起了吗？commit 合规吗？相关 Sensor 复验了吗？关键 Behaviour 有独立证据或明确的人类验收吗？

**裁剪**：问题条目按项目增删，「全是才能合」的形式必留。

---

## 机制 10 —— Control Map + Steering Loop

**问题**：原有红线三列表能证明硬门禁有牙齿，但仍回答不了三件事：软约束由谁 review、关键行为靠什么独立证据验收、同类错误重复发生后谁升级 Harness。

**做法**：实例化 [`templates/docs/harness-controls.template.md`](templates/docs/harness-controls.template.md)，维护三组轻量记录和一组引用：

- **覆盖边界**：Maintainability、Architecture Fitness、Behaviour 各自覆盖到哪里，明确不保证什么。
- **Control Map**：最小只填目标 → Guide → Sensor / 人工确认 → 失败处置 → Owner；类型、目标类别和生命周期仅在审计发现歧义时追加。
- **Behaviour Evidence 引用**：证据唯一写在 `SPEC.md`，Controls 只保存用例锚点与相关 Control，避免双写。
- **Steering Log**：只有同类失败至少出现两次或形成趋势证据后才记录；初始化时不建空台账。

约束分三级，不把所有重要事情都硬塞进 grep：

1. `Deterministic Gate`：能稳定机械判断，违反必拦。
2. `Inferential Review Criterion`：需要语义与权衡，输出证据和建议。
3. `Human Acceptance Decision`：涉及业务意图、风险和责任，由明确责任人签收。

**裁剪**：小项目可只保留 3–5 行 Control Map 和一段覆盖边界；可以裁行数，不能裁“重要目标必须有检测或人工确认路径”这个原则。

---

## 怎么裁剪：按项目规模

| 规模 | 建议取哪些机制 |
| --- | --- |
| 个人脚本 / 小工具 | 1（AGENTS）+ 2 精简版红线 |
| 单人/小队产品 | 1 + 2 + 4（workflow）+ 7（commit）+ 5（ADR 按需）+ 精简 Control Map |
| 多人 + 真实业务方 | 全部 11 个，Behaviour evidence 不可省 |
| 替换型 / 强约束迁移项目 | 全部 11 个，且红线要写「禁止旧依赖复活」并维护 baseline |

> 原则：**机制是用来减少漂移的，不是用来摆样子的。** 没人查的契约比没有契约更糟——它制造「我们有规矩」的假象。每加一条红线、一个场景、一张卡，都要能回答「谁来查、怎么查」。
