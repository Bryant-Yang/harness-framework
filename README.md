# Harness Framework —— 「文档即契约」协作脚手架

> 作者：Bryant Yang
>
> 这是一套从 `dw_gis3d` 工程沉淀出来的**通用工程契约框架**，与具体技术栈无关。
> 它解决一个问题：**让任何 AI 编码 agent 进场即知道「这是什么项目、不能碰什么、产出落在哪、提交前必跑什么」**，而不是每个会话重新解释一遍。

> **读者是 agent,不是人。** Claude Code / Codex / Cursor / Gemini CLI / Google 反重力 Antigravity 等各家工具找的入口文件名不同(`CLAUDE.md` / `AGENTS.md` / `GEMINI.md` …)。本框架以 `AGENTS.md` 为**唯一契约源**(已是 Linux 基金会主推的开放标准,20+ 工具原生读取),其余工具用**薄指针文件**指回它——见下方「机制 0」。

---

## 这套框架是什么

它不是代码库，而是一组**文档模板 + 协作机制**。核心思想：

> **把项目的「钢印级约束」固化成可 grep、可驳回、可索引的文档，而不是散落在人脑和聊天记录里。**

10 个可复用机制（详见 [`METHODOLOGY.md`](METHODOLOGY.md)）：

| # | 机制 | 模板文件 | 一句话作用 |
| --- | --- | --- | --- |
| 0 | **多工具入口指针** | `CLAUDE.md` / `GEMINI.md` / `.github/` / `.cursor/` | 每个 agent 工具找的文件名不同，各放一个薄指针指回 AGENTS.md |
| 1 | **唯一契约源** | `AGENTS.template.md` | 真正的契约只此一份，所有指针都引到它，杜绝多份漂移 |
| 2 | **工程契约（北极星 + 红线）** | `HARNESS.template.md` | 北极星原则 + 技术栈基线 + 目录约束 + **红线 N 条**（驳回级硬约束） |
| 2.5 | **红线守门（牙齿）** | `enforcement/` | 把红线编译成 grep / lint / commitlint / CI 闸门——违反就合不进。**没这层红线是装饰** |
| 3 | **业务规格总纲** | `docs/SPEC.template.md` | 用例索引 + 用例模板 + 阶段一览，业务/开发的共同语言 |
| 4 | **场景化工作流表** | `docs/workflow.template.md` | 「我属于哪种任务」→ 先读哪份 / 守哪条红线 / 产出在哪 / DoD 是什么 |
| 5 | **ADR 决策记录** | `docs/adr/` | 工程「为什么这么做」的不可变档案；改契约先开 ADR |
| 6 | **业务决议卡** | `docs/decisions/` | 业务「系统该做什么」的待决问题，⏳ 状态可阻断里程碑 |
| 7 | **提交规范** | `docs/git-commit-conventions.template.md` | Conventional Commits，CI commitlint 强制 |
| 8 | **文档地图（按角色）** | `PROJECT-README.template.md` | 不同角色/任务的文档入口表 |
| 9 | **提交前自查清单** | 内嵌于 workflow / AGENTS | 六问全「是」才能 request review |

---

## 机制 0 —— 多工具入口（agent-first 的关键）

各家工具自动发现的入口文件名不同。本框架的策略：**`AGENTS.md` 一份真契约,其余全是指针**。

| 工具 | 它自动找的文件 | 原生读 `AGENTS.md`? | 框架放什么 |
| --- | --- | --- | --- |
| **Codex CLI** | `AGENTS.md` | ✅ 原生 | 真契约,无需额外 |
| **Cursor** | `AGENTS.md`（亦支持 `.cursor/rules/*.mdc`） | ✅ 原生 | 可选 `.cursor/rules/000-agents.mdc` 指针（旧版/优先级需要时） |
| **GitHub Copilot** | `AGENTS.md` / `.github/copilot-instructions.md` | ✅ 原生 | 可选 `.github/copilot-instructions.md` 指针 |
| **Windsurf / Amp / Devin / Zed / Aider / Jules / Junie 等** | `AGENTS.md` | ✅ 原生 | 真契约,无需额外 |
| **Google 反重力 Antigravity** | `GEMINI.md`（最高）→ `AGENTS.md` → `.agent/rules/` | ✅ 原生（低优先级） | 放 `GEMINI.md` 薄指针,避免被空覆盖 |
| **Gemini CLI** | `GEMINI.md` | ❌ | **必须** `GEMINI.md` 指针（`@AGENTS.md` 导入） |
| **Claude Code** | `CLAUDE.md` | ❌（pending） | **必须** `CLAUDE.md` 指针（`@AGENTS.md` 导入） |

> 原则:**指针只指,不写规则**。任何指针文件里出现实质规则,就是漂移的开始——立刻搬回 `AGENTS.md`。
> 数据来源:[agents.md 开放标准](https://agents.md/)、Antigravity 官方文档(v1.20.3 起读 AGENTS.md)。各家支持随版本变化,落地前核对当时文档。

---

## 目录结构

```
harness_extract/
├── README.md                          # 本文：框架是什么 + 如何实例化
├── METHODOLOGY.md                     # 方法论：每个机制为什么存在、如何裁剪
├── AI-ADOPTION-PROTOCOL.md            # AI 自动接入协议：新旧项目统一落地流程
├── INSTANTIATION-CHECKLIST.md         # 复用到新工程的逐步检查清单
└── templates/                         # 拷过去即可（带 <占位符> 的填空，指针文件直接用）
    ├── AGENTS.template.md              # ← 唯一真契约（机制 1）
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

examples/node-orders-api/              # 异构完整样例：Node 后端，红线全填好
├── README.md                          #   对照「机制相同、内容不同」
├── HARNESS-redlines.md                #   §8 三列表填好版
├── workflow-scenes.md                 #   场景表填好版
└── scripts/check-redlines.sh          #   可运行、已验证能拦违规
```

---

## 如何复用到新工程（30 秒版）

1. 把 `templates/` 整份拷到新工程根目录。
2. 全局替换占位符（见每个模板顶部的「占位符清单」）：
   - `<PROJECT>` → 你的项目名
   - `<MISSION>` → 项目使命一句话
   - `<STACK_*>` → 技术栈选型
   - 红线、目录、场景表按项目实情增删。
3. 删掉每个模板里标了 `> 示例（dw_gis3d）：` 的引用块——那只是给你看「填成什么样」。
4. 把 `*.template.md` 重命名去掉 `.template`（如 `AGENTS.template.md` → `AGENTS.md`）。
5. 在每个 agent 的私有配置里加一行 `@AGENTS.md`（指针，机制 1）。
6. 跟着 [`INSTANTIATION-CHECKLIST.md`](INSTANTIATION-CHECKLIST.md) 逐条核对。

> **给团队的说明**：`*.template.md` 文件正文里的内部链接（如 `HARNESS.md`、`docs/workflow.md`）
> 指向的是**改名实例化之后**的文件，所以在 `templates/` 里直接点会显示「找不到」——这是正常的。
> 第 4 步把 `.template` 去掉后，全部链接自动解析。不要因为模板里「链接打不开」以为框架坏了。

> 完整方法论与裁剪建议见 [`METHODOLOGY.md`](METHODOLOGY.md)。
> 小项目可只取机制 1/2/2.5/4/7（AGENTS + HARNESS + **enforcement** + workflow + commit），其余按规模长出来。
> **但机制 2.5 守门不能省**——红线没有闸门就是装饰，是 harness「有效」还是「摆设」的分水岭。
>
> 想看填好的成品长什么样？读 [`examples/node-orders-api/`](examples/node-orders-api/)（一个异构的 Node 后端样例）。

## 如何让 AI 自动接入

新旧项目都可以按 [`AI-ADOPTION-PROTOCOL.md`](AI-ADOPTION-PROTOCOL.md) 执行。核心流程固定为：

```text
发现项目事实 → 实例化文档 → 生成红线 → 接 enforcement → 负向验证 → 输出未决项
```

把协议里的「给 AI 的固定指令」交给 Codex / Claude Code / Gemini CLI 等 agent，即可让 AI 自动审计项目、填充模板、接红线守门并完成负向验证。
