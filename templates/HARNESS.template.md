# <PROJECT> 工程契约（HARNESS）

> 作者：<AUTHOR>　最近更新：<YYYY-MM-DD>　Harness Framework：2.0.1（来源 commit：<sha>）
>
> 这是 **工程侧的契约文档**：北极星原则、技术栈、目录结构、红线、决策入口。配套 [`docs/SPEC.md`](docs/SPEC.md)（业务规格）与 [`docs/workflow.md`](docs/workflow.md)（按场景的工作流）。
>
> 业务 / 产品同事请直接看 SPEC.md；本文是写代码、改架构、合 PR 的钢印。

<!--
占位符清单：<PROJECT> <AUTHOR> <MISSION> 技术栈表 目录树 红线条目 性能预算。
红线编写黄金标准：能写成一条 grep 命令的才是红线，否则降级到北极星或普通规范。
-->

## 文档地图

| 你要做什么 | 直接读 |
| --- | --- |
| 了解全貌 | [`README.md`](README.md) → [`docs/workflow.md`](docs/workflow.md) |
| 看用例（业务） | [`docs/SPEC.md`](docs/SPEC.md) |
| 看依赖与配置 | [`docs/deps-and-configs.md`](docs/deps-and-configs.md) |
| 看里程碑 / DoD | [`docs/roadmap.md`](docs/roadmap.md) |
| 起决策 | [`docs/adr/README.md`](docs/adr/README.md) |
| 业务决议 | [`docs/decisions/README.md`](docs/decisions/README.md) |
| 看 Guide / Sensor / Steering 闭环 | [`docs/harness-controls.md`](docs/harness-controls.md) |

---

## 0.0 项目使命（不可让步）

<用 2–4 句写清「完工口径」是什么——不是模糊愿景，而是可验收的终态。如果项目是替换/迁移型，写清「旧依赖在何处被删除、CI 如何守门防回归」。>

这条使命在任何阶段优先级 > 单个新功能优先级。

> 示例（dw_gis3d）：使命是彻底替代 HT 商业库——能力对等 + 接口透明 + 依赖卸载，终态组织内不再有任何 HT 运行时与 license 占用。

## 0. 北极星原则

> 项目级价值排序。两个做法冲突时用它裁决。建议 5–7 条。

| 原则 | 解释 |
| --- | --- |
| 单一来源 | 一种坐标系、一种时间格式、一种事件总线、一种 i18n。不并存多套方案。 |
| 边界先行 | 先定层间契约，再写实现。 |
| 可测胜过可看 | 核心逻辑必须有单测；UI 用集成测试覆盖关键路径。 |
| 反 God-Class | 任何文件 > <N> 行视为重构信号。 |
| 显式状态机 | 复杂交互以 FSM 表达，禁止散落布尔标志。 |
| 性能预算 | 关键指标有明确上限，不达标即未完成。 |

## 1. 技术栈与版本基线

| 类别 | 选型 |
| --- | --- |
| 框架 | <...> |
| 语言 | <...> |
| 构建 | <...> |
| 状态 | <...> |
| 测试 | <...> |
| Lint | <...> |
| 包管理 | <...> |

**不允许的依赖**：<列出明确拉黑的库，包括「同类第二套」与被替换的旧库>。

## 2. 目录结构

```text
<PROJECT>/
├── HARNESS.md
├── README.md
├── docs/
└── src/
    └── <按你的分层画出来>
```

**约束（违反即驳回）：**

- <分层单向依赖约束，例如 `modules/` 禁止 `import '<重依赖>'`>
- <哪一层不准依赖哪一层>

## 3. 工程规范

脚本、Lint 配置、Prettier、Git/提交规范、CI 阶段、依赖与配置模板：见 [`docs/deps-and-configs.md`](docs/deps-and-configs.md)。

提交侧硬约束：

- `git add` 必须显式列出文件，禁止 `git add .` / `git add -A`；
- Commit message 走 Conventional Commits；
- 单 PR 改动行数 > <M> 视为拆分信号；
- CI 必走 `<CI_CMD>`，缺一不合。

## 4. 技术架构

### 4.1 分层模型

```
<画出层间单向依赖箭头>
```

任何反向依赖在 PR 中视为架构违规。

### 4.2 ~ 4.N 各层封装规范

<逐层写关键约束：入口工厂、禁止的写法、必须走的统一入口、反应性/资源清理红线等。每层一小节。>

### 4.x 错误处理与可观测性

<异步初始化必须 try/catch + 统一 notify；自定义 DomainError；统一日志入口；关键交互打点。>

## 5. 数据契约与配置入口

跨模块数据结构、消息信封、配置项与依赖白/黑名单不在本文重复维护：

- 数据契约见 [`docs/data-contracts.md`](docs/data-contracts.md)；
- 依赖与配置见 [`docs/deps-and-configs.md`](docs/deps-and-configs.md)。

修改这些契约时，必须同步更新调用方、测试和必要 ADR。

## 6. 质量门禁

CI 与本地提交前检查按同一顺序执行：

```text
redlines → typecheck → lint → test → build
```

任何阶段失败都视为未完成；不得用 `--no-verify` 或跳过脚本绕过门禁。

完整控制闭环见 [`docs/harness-controls.md`](docs/harness-controls.md)：硬门禁只登记可稳定机械判断的约束；语义与权衡进入 Inferential Review；业务意图与风险由明确责任人验收。

## 7. 测试策略

| 层级 | 工具 | 环境 |
| --- | --- | --- |
| 单测 | <...> | <...> |
| 组件 | <...> | <...> |
| 集成 | <...> | <...> |
| E2E | <...> | <...> |

**约束：**

- <环境陷阱，例如「不允许用 jsdom 测 WebGL，会假性绿」>
- 测试不允许从公网拉数据；走本地 fixtures。
- 资源在 `beforeEach` setup、`afterEach` 销毁，验证 mount/unmount 不泄漏。
- 关键 Behaviour 必须有至少一种独立证据来源；当前实现 agent 新生成的测试不能成为唯一验收证据。

## 8. 红线（共 <N> 条，违反必驳回）

> **强制规则**：每条红线**必须**填满「守门命令」列——它就是 [`enforcement/`](enforcement/) 里那一行
> grep / lint / commitlint。**填不出守门命令的不准当红线**，降级到北极星原则或普通规范。
> 违反不讨论例外，直接 reject。宁少勿滥：10 条真红线 > 30 条没人查的红线。

| # | 红线 | 守门命令（一一对应 `enforcement/`） | 谁拦 |
| --- | --- | --- | --- |
| R1 | 禁止类型逃逸（`as any` / `as unknown as`） | `check "R1" ... '\bas any\b\|as unknown as'` + eslint `no-explicit-any` | grep + lint |
| R2 | 不允许同时引入第二套 <UI/状态/网络> 库 | `no-restricted-imports` regex 禁 `<lib-a>\|<lib-b>` | lint |
| R3 | 被替换的旧依赖禁止任何形式复活 | `no-restricted-imports` regex 禁 `^<legacy>` | lint |
| R4 | 业务层禁止裸 import <重依赖>（必须走封装层） | `no-restricted-imports`（业务目录禁、封装层豁免） | lint |
| R5 | 新代码无单测不进主分支 | CI `pnpm test` + coverage 阈值 | CI |
| R6 | commit 必走 Conventional Commits | `commitlint` type-enum | commit-msg 钩子 |
| R7 | <项目特有红线，例如「文案必须接 t()」> | `check "R7" ... '<grep 模式>'` | grep |
| R8 | 不写 God Class（文件 > <N> 行先拆） | `check "R8"`（行数脚本）或 code review | grep/review |

> **每加一条红线，先问「谁来查、用什么命令查」。** 答不上来就不是红线。
> 配套守门实现见 [`enforcement/README.md`](enforcement/README.md)。
> 写不出机械命令不代表不重要：语义约束登记为 `docs/harness-controls.md` 的 Inferential Review Criterion，业务与风险登记为 Human Acceptance Decision。

## 9. 决策记录（ADR）

每个重大决定写一篇 ADR，模板见 [`docs/adr/_template.md`](docs/adr/_template.md)，索引见 [`docs/adr/README.md`](docs/adr/README.md)。ADR 正文一经合入只能通过新 ADR（标记 `Supersedes`）修订；不允许直接编辑旧 ADR 正文。ADR 索引可更新状态与交叉引用。

## 10. Harness 控制闭环

控制台账见 [`docs/harness-controls.md`](docs/harness-controls.md)。至少维护：

- 三类目标的覆盖边界与明确不保证项；
- 重要目标的 Guide、Sensor / 人工确认、失败处置和 Owner；疑难项才追加类型与生命周期；
- 指向 `SPEC.md` 中关键 Behaviour 独立验收证据的引用；
- 达到触发条件后才建立的 Steering 记录；
- Legacy baseline 与模板升级记录。

## 11. 入门 Checklist（新成员第一周）

- [ ] 通读本文 §0.0 → §10，使命能用一句话复述
- [ ] 阅读启动期关键 ADR
- [ ] 跑通 `<本地 dev / test / build 命令>`
- [ ] 提交一个不超过 100 行的 PR（修文档 / 加单测 / 修类型）熟悉流程

---

*本文是动态合约。每次重大改动须同步更新本文与相关 ADR。*
