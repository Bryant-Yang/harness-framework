# Harness Framework 2.3.0 —— 「文档即契约」到「可学习控制闭环」

> 作者：Bryant Yang
>
> 这是一套从 `dw_gis3d` 工程沉淀出来的**通用工程契约框架**，与具体技术栈无关。
> 它解决一个问题：**让任何 AI 编码 agent 进场即知道「这是什么项目、不能碰什么、产出落在哪、提交前必跑什么」；做完后还能被 Sensor 检测、自我修正，并把重复失败反馈到下一版契约。**

> **读者是 agent,不是人。** Claude Code / Codex / Cursor / Gemini CLI / Google 反重力 Antigravity 等各家工具找的入口文件名不同(`CLAUDE.md` / `AGENTS.md` / `GEMINI.md` …)。本框架以 `AGENTS.md` 为**唯一项目入口**(已是 Linux 基金会主推的开放标准,20+ 工具原生读取),其余工具用**薄指针文件**指回它——见下方「机制 0」。

---

## 这套框架是什么

它不是代码库，而是一组**文档模板 + 协作机制**。核心思想：

> **把项目方向和「钢印级约束」固化成可路由的 Guides，把关键风险编译成可执行的 Sensors，再用 Self-correction 与 Candidate-first Experience Promotion 形成可学习闭环。**

2.0 在原有 docs-as-contract 与红线 enforcement 之上补齐了 Harness Engineering 的上位模型：

```text
Guide 预先引导 → Agent 变更 → Sensor 检测 → Agent 自我修正
       ↑                                      │
       └── Evidence → Candidate → Eval → Owner：稳定经验晋级 ─┘
```

完整概念与边界见 [`docs/HARNESS-ENGINEERING.md`](docs/HARNESS-ENGINEERING.md)。框架仍然是方法与契约库，不是重型 agent 编排平台。

2.1 补充三项不增加日常负担的维护能力：已接入项目按变更影响做增量维护；仅在项目实际存在 Agent / Skill / 编排资产时审计悬空引用、职责重叠与复用机会；关键边界的 Sensor 同时验证 producer 实际输出、contract / transform 与 consumer 预期。它们不新增机制编号、目标项目文件、日常必做步骤或 CI 任务。

2.2 把这条闭环向前后各延伸一步，但**不改变使用入口**：

- 开工时按 `always-on / task-loaded / phase-loaded` 路由上下文，并用 Routing Probe 检查有没有漏载关键事实；
- 在现有 `HARNESS.md §0.0` 内明确 Direction Contract：当前基线、目标状态、不变量 / 非目标、关闭证据与变更权限；
- 重复失败或高严重度逃逸先生成带证据的 Candidate，经反例评测和 Owner 批准后，才晋级为 Guide、Sensor、Skill 或 Gate；
- 项目实际存在 Codex Goal、Mission Driver 等 runner 时，才补一段可选 Consumption Contract；Harness 仍不承担运行时编排。

已有 2.1 项目可增量吸收；没有新命令、日常清单、强制顶层文件或空台账。正常任务仍然从 `AGENTS.md → workflow 场景` 进入，只有出现高价值候选、上下文冲突或高风险边界时才增加可见反馈。

2.3 将这些要求变成可回放的交付：

- 检查区分 PASS / FAIL / ERROR，漏配和扫描错误阻断；每条文本规则、baseline、TS 与 commitlint 都有实际探针，grep 的语义边界明确。
- [经验学习](docs/experience-learning.md)采用首个事件引用、按任务召回、稳定 ID、候选 / 评测 / 生效 / 退役；[真实样例](examples/experience-loop/README.md)回放旧脚本假绿。Skill 模型 A/B 尚未运行，门禁回放不代表模型收益。
- [最小 / 产品组合](docs/instantiation-profiles.md)让裁剪后的文档和锚点闭合；旧项目只合并必要改动，已批准 baseline 只拦新增。当前 HARNESS 可维护，Accepted ADR 保存历史。
- Skill 同步先完整暂存并验证，再替换目标；保留共享符号链接、旧版本备份和内容清单，可只读检查漂移。

11 个可复用机制（详见 [`METHODOLOGY.md`](METHODOLOGY.md)）：

| # | 机制 | 模板文件 | 一句话作用 |
| --- | --- | --- | --- |
| 0 | **多工具入口指针** | `CLAUDE.md` / `GEMINI.md` / `.github/` / `.cursor/` | 每个 agent 工具找的文件名不同，各放一个薄指针指回 AGENTS.md |
| 1 | **唯一项目入口** | `AGENTS.template.md` | 入口只此一份，事实分别由 Owner Doc 持有，指针只路由 |
| 2 | **工程契约（方向 + 北极星 + 红线）** | `HARNESS.template.md` | 用轻量 Direction Contract 冻结目标与关闭证据，再声明北极星、技术栈、目录和驳回级红线 |
| 2.5 | **红线守门（牙齿）** | `enforcement/` | 把红线编译成 grep / lint / commitlint / CI 闸门——违反就合不进。**没这层红线是装饰** |
| 3 | **业务规格总纲** | `docs/SPEC.template.md` | 用例索引 + 用例模板 + 阶段一览，业务/开发的共同语言 |
| 4 | **场景化工作流 + 上下文路由** | `docs/workflow.template.md` | 「我属于哪种任务」→ 只装入该任务 / 阶段所需事实，并用 Routing Probe 防漏载 |
| 5 | **ADR 决策记录** | `docs/adr/` | 工程「为什么这么做」的不可变档案；改契约先开 ADR |
| 6 | **业务决议卡** | `docs/decisions/` | 业务「系统该做什么」的待决问题，⏳ 状态可阻断里程碑 |
| 7 | **提交规范** | `docs/git-commit-conventions.template.md` | Conventional Commits，CI commitlint 强制 |
| 8 | **文档地图（按角色）** | `PROJECT-README.template.md` | 不同角色/任务的文档入口表 |
| 9 | **提交前自查清单** | 内嵌于 workflow / AGENTS | 适用项通过；失败、未运行和不适用分别报告 |
| 10 | **控制台账 + Experience Promotion** | `docs/harness-controls.template.md` | 最小登记控制；稳定经验先成为 Candidate，经评测与批准后再晋级，runner 契约按存在性启用 |

---

## 机制 0 —— 多工具入口（agent-first 的关键）

各家工具自动发现的入口文件名不同。本框架的策略：**`AGENTS.md` 一个入口，事实由指定 Owner Doc 持有，其余工具配置保持薄指针**。

| 工具 | 它自动找的文件 | 原生读 `AGENTS.md`? | 框架放什么 |
| --- | --- | --- | --- |
| **Codex CLI** | `AGENTS.md` | ✅ 原生 | 真契约,无需额外 |
| **Cursor** | `AGENTS.md`（亦支持 `.cursor/rules/*.mdc`） | ✅ 原生 | 可选 `.cursor/rules/000-agents.mdc` 指针（旧版/优先级需要时） |
| **GitHub Copilot** | `AGENTS.md` / `.github/copilot-instructions.md` | ✅ 原生 | 可选 `.github/copilot-instructions.md` 指针 |
| **Windsurf / Amp / Devin / Zed / Aider / Jules / Junie 等** | `AGENTS.md` | ✅ 原生 | 真契约,无需额外 |
| **Google 反重力 Antigravity** | `GEMINI.md`（最高）→ `AGENTS.md` → `.agent/rules/` | ✅ 原生（低优先级） | 放 `GEMINI.md` 薄指针,避免被空覆盖 |
| **Gemini CLI** | `GEMINI.md` | ❌ | **必须** `GEMINI.md` 指针（`@AGENTS.md` 导入） |
| **Claude Code** | `CLAUDE.md` | ❌（pending） | **必须** `CLAUDE.md` 指针（`@AGENTS.md` 导入） |

> 原则:**指针只指,不写规则**。任何指针文件里出现实质规则,就是漂移的开始——搬回对应 Owner Doc，由 `AGENTS.md` 路由。
> 数据来源:[agents.md 开放标准](https://agents.md/)、Antigravity 官方文档(v1.20.3 起读 AGENTS.md)。各家支持随版本变化,落地前核对当时文档。

---

## 目录结构

```
harness-framework/
├── VERSION                            # 框架版本
├── README.md                          # 本文：框架是什么 + 如何实例化
├── METHODOLOGY.md                     # 方法论：每个机制为什么存在、如何裁剪
├── docs/HARNESS-ENGINEERING.md        # Direction / Context / Guides / Sensors / Experience 上位模型
├── docs/MISSION-DRIVER-AGE-COMMUNICATION-KB.md # 2.2 外部研究与证据边界（非规范）
├── AI-ADOPTION-PROTOCOL.md            # AI 自动接入与增量维护协议
├── INSTANTIATION-CHECKLIST.md         # 复用到新工程的逐步检查清单
├── LICENSE                            # MIT
├── SKILL.md                           # 标准 skill 根入口；npx 安装时携带本仓完整资源
├── .github/workflows/check-framework.yml # 本仓自证 CI，执行隔离探针与锁定 TS / commitlint
├── scripts/check-framework.sh         # 结构、锚点、实例化、baseline、回放与安装探针入口
├── scripts/sync-skill.sh             # 仓库维护者本地组装、同步 skill 的兼容脚本
└── templates/                         # 拷过去即可（带 <占位符> 的填空，指针文件直接用）
    ├── AGENTS.template.md              # ← 唯一项目入口（机制 1）
    ├── CLAUDE.md                       # ┐
    ├── GEMINI.md                       # │ 机制 0：多工具入口指针，内容只指回 AGENTS.md
    ├── .github/copilot-instructions.md # │
    ├── .cursor/rules/000-agents.mdc    # ┘
    ├── HARNESS.template.md
    ├── PROJECT-README.template.md
    ├── enforcement/                    # ← 红线的牙齿（机制 2.5）
    │   ├── README.md                   #   接线 + 黄金判据 + 跨语言抽象
    │   ├── scripts/check-redlines.sh   #   【语言无关】grep 闸门，改后缀即跨语言
    │   ├── commitlint.config.cjs       #   【语言无关】
    │   ├── ci.yml                      #   骨架：redlines→typecheck→lint→test→build
    │   ├── ts/eslint.config.skeleton.ts   #   JS/TS：no-restricted-imports
    │   ├── java/ArchUnitRedlinesTest.java #   Java：ArchUnit 分层/禁依赖
    │   └── python/pyproject-redlines.toml #   Python：import-linter + ruff + mypy
    └── docs/
        ├── SPEC.template.md
        ├── workflow.template.md
        ├── harness-controls.template.md # 控制台账 + SPEC 引用 + Candidate-first 经验晋级
        ├── git-commit-conventions.template.md
        ├── roadmap.template.md           # 支撑文档：里程碑 + DoD
        ├── deps-and-configs.template.md  # 支撑文档：依赖白/黑名单 + 配置
        ├── data-contracts.template.md    # 支撑文档：跨模块数据结构
        ├── glossary.template.md          # 支撑文档：术语速查
        ├── adr/
        │   ├── README.template.md
        │   └── _template.md
        └── decisions/
            └── README.template.md

examples/node-orders-api/              # 假想 Node 后端样例：字段完整，检测边界明确
├── README.md                          #   对照「机制相同、内容不同」
├── HARNESS-redlines.md                #   §8 三列表填好版
├── workflow-scenes.md                 #   场景表填好版
├── SPEC.md                            #   Behaviour Evidence 唯一事实源节选
├── harness-controls.md                #   Control Map、SPEC 引用与 Experience Promotion
└── scripts/check-redlines.sh          #   可运行、已验证能拦违规
```

---

## 如何复用到新工程（30 秒版）

1. 按[实例化组合](docs/instantiation-profiles.md)选择必要模板；小工具用 `templates/minimal/`，产品按实际范围使用根模板。旧项目在已有事实源最小合并，禁止整份覆盖。
2. 全局替换占位符（见每个模板顶部的「占位符清单」）：
   - `<PROJECT>` → 你的项目名
   - `<MISSION>` → 项目使命一句话
   - `<STACK_*>` → 技术栈选型
   - 红线、目录、场景表按项目实情增删。
3. 删掉每个模板里标了 `> 示例（dw_gis3d）：` 的引用块——那只是给你看「填成什么样」。
4. 把 `*.template.md` 重命名去掉 `.template`（如 `AGENTS.template.md` → `AGENTS.md`）。
5. 仅为实际需要的工具加入薄指针；原生读取 AGENTS 的工具不额外复制规则。
6. 跟着 [`INSTANTIATION-CHECKLIST.md`](INSTANTIATION-CHECKLIST.md) 逐条核对。

> **给团队的说明**：`*.template.md` 文件正文里的内部链接（如 `HARNESS.md`、`docs/workflow.md`）
> 指向的是**改名实例化之后**的文件，所以在 `templates/` 里直接点会显示「找不到」——这是正常的。
> 第 4 步把 `.template` 去掉后，全部链接自动解析。不要因为模板里「链接打不开」以为框架坏了。

> 完整方法论与裁剪建议见 [`METHODOLOGY.md`](METHODOLOGY.md)。
> 小项目使用闭合的最小组合；仅对启用的机械红线接门禁，不凑规则数量。删去未采用的 SPEC / ADR / 里程碑引用，并运行实例化检查。
>
> 想看填好的成品长什么样？读 [`examples/node-orders-api/`](examples/node-orders-api/)（一个异构的 Node 后端样例）。

## 如何让 AI 自动接入或维护

新旧项目首次接入、已接入项目后续维护都按 [`AI-ADOPTION-PROTOCOL.md`](AI-ADOPTION-PROTOCOL.md) 执行。首次接入核心流程为：

```text
发现事实与 Harnessability → 冻结方向 / 路由上下文 → 实例化文档 → 建 Control Map
→ 生成红线并接 enforcement → 负向验证与自修 → 在 SPEC 补行为证据
→ 按触发条件输出 Experience Candidate / 未决项
```

把协议里的「给 AI 的固定指令」交给 Codex / Claude Code / Gemini CLI 等 agent，即可让 AI 自动审计项目、填充模板、接红线守门并完成负向验证。

已经完成实例化的项目不重跑整套接入流程。修改控制、Context Routing、Experience Candidate、Runner Consumption 或 AI-facing 资产时，按协议的[维护矩阵](AI-ADOPTION-PROTOCOL.md#已接入项目维护口径)只同步受影响的事实源、引用和配套控制；普通业务改动不会额外触发 Harness 维护步骤。

## 作为 skill 安装（一键触发，免手动翻协议）

本框架已封装成 [agentskills.io](https://agentskills.io) 格式的 skill，让 Claude Code / Codex
在**任意新旧项目**里被自动发现并触发——不必每次手动把协议贴给 agent。

```bash
npx skills add Bryant-Yang/harness-framework \
  --skill harness-framework \
  -g \
  -a codex \
  -a claude-code \
  -y
```

该命令直接从 GitHub 安装，并把同一份完整 skill（入口、模板、样例和方法文档）链接到 Codex 与 Claude Code 的全局技能目录。
安装前想先确认仓库中可用的 skill：

```bash
npx skills add Bryant-Yang/harness-framework --list
```

以后更新到仓库最新版：

```bash
npx skills update harness-framework -g -y
```

- **Claude Code**：在目标项目里说「用 harness 给这个项目立规矩」，或直接 `/harness-framework`。
- **Codex**：同名 skill 已就位，触发方式一致。


## 维护与验证

```bash
npm ci --prefix tests/enforcement/ts --ignore-scripts
bash scripts/check-framework.sh --with-toolchains
# stdlib 结构 / shell / baseline / 回放检查，不执行 TS
bash scripts/check-framework.sh
# 同步现有全局 Skill；已有链接共享时只更新一次，保留旧版备份
bash scripts/sync-skill.sh
bash scripts/sync-skill.sh --check
```

需要 Python 3.10+、Bash、grep；toolchain fixture 使用锁定 npm 依赖，Node 22.13+。新脚本位于 `scripts/`，工具链样例位于 `tests/enforcement/ts/`。CI 执行同一完整命令。安装内容清单记录版本、来源 commit、源工作树状态和文件哈希；备份放在技能根目录外的 `skill-backups/`。修改已安装副本会被 `--check` 检出，修改应回到仓库后同步。

验证边界：文档闭合不证明语义路由完整；文本 smoke 不证明 AST 覆盖；业务样例是虚构设定；Java / Python 的专用 lint / ArchUnit toolchain 和模型 Skill A/B 本轮未运行。
