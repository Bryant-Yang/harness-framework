# AI 自动接入协议 —— 新旧项目如何使用 Harness

> 作者：Bryant Yang
>
> 本文把 harness 的使用方式固化成一套 AI 可执行协议。无论新项目还是旧项目，都让 AI 按这套流程完成：
> **审计事实与 Harnessability → 实例化文档 → 建 Control Map → 生成红线 → 接 enforcement → 负向验证与自修 → 在 SPEC 补行为证据 → 按触发条件输出 Steering 与未决项**。

## 适用场景

- 新项目：从空仓库或早期骨架开始，把 harness 一次性铺好。
- 旧项目：已有代码、README、CI、约定和历史债，把 harness 接进去但不破坏现状。
- 迁移 / 替换项目：需要禁止旧依赖复活，且希望 AI 每次进场都能守住边界。

## 核心原则

1. AI 负责判断与填空：审计现状、识别分层、抽取风险、写出红线候选。
2. 脚本负责确定性动作：复制模板、替换占位符、grep 红线、跑验证。
3. CI 负责最终兜底：违反红线时合不进主分支。
4. 旧项目不暴力覆盖：已有文档先保留，冲突时生成候选版本或合并。
5. 红线必须可执行：写不出 grep / lint / CI 守门的，不准叫红线。
6. 重要目标必须闭环：行动前有 Guide，行动后有 Sensor 或明确的人类确认路径。
7. 约束分级：确定性 Gate、推理型 Review Criterion、人类 Acceptance Decision 不混用。
8. 行为证据独立：当前实现 agent 自己生成的测试不能成为关键行为的唯一验收依据。

## 统一流水线

```text
1. Project Audit + Harnessability
   识别技术栈、目录结构、构建/测试/lint/CI、现有 agent 配置、类型反馈、模块边界、
   测试隔离性、运行日志和关键行为证据。

2. Harness Instantiation
   生成或合并 AGENTS.md、HARNESS.md、docs/workflow.md、docs/harness-controls.md、
   commit 规范和必要指针文件，并记录框架版本与本地差异。

3. Control Mapping
   把重要目标最小映射为 Guide、Sensor / 人工确认、失败处置和 Owner；
   用覆盖边界审计 Maintainability / Architecture Fitness / Behaviour，只对疑难 Control 追加类型与生命周期注记。

4. Redline Design
   从项目风险里提炼 3-8 条可机械检查的红线，并登记到 HARNESS §8。

5. Enforcement Wiring
   为每条红线接 grep / lint / commitlint / CI 守门。

6. Negative Verification + Self-correction
   故意写一条违规探针，确认守门失败且反馈足以指导修复；删除探针，再确认守门通过。

7. Behaviour Evidence
   在 SPEC 对关键用例登记独立证据、批准人和人工边界；Controls 只引用用例，不双写证据。

8. Handoff + Steering
   输出已接好的控制、红线、覆盖边界、历史债 baseline 和人工待决；只有同类失败至少两次或已有趋势证据时才输出 Steering。
```

## 新项目执行口径

新项目可以直接实例化完整骨架：

- 复制 `templates/` 到项目根目录。
- `*.template.md` 去掉 `.template`。
- 将框架版本与来源 commit 记录到 `docs/harness-controls.md`。
- 填入 `<PROJECT>`、`<AUTHOR>`、`<MISSION>`、`<YYYY-MM-DD>`、`<语言>`、`<CI_CMD>`。
- 先写 3-5 条红线，不要一开始堆满。
- 直接把 enforcement 接进 CI。
- 对至少一个关键行为在 `SPEC.md` 登记独立验收证据；没有真实业务的工具库可标记为“不适用”。

完成标准：

- `AGENTS.md` 是唯一契约源。
- `HARNESS.md §8` 每条红线都有守门命令。
- `docs/harness-controls.md` 里的重要目标都有 Sensor 或明确的人类确认路径。
- `bash scripts/check-redlines.sh` 能通过。
- 负向违规探针能被拦住。

## 旧项目执行口径

旧项目先审计，再接入：

- 不覆盖已有 `README.md`、`AGENTS.md`、`CLAUDE.md`、`GEMINI.md`、CI 配置。
- 冲突时生成候选文件，如 `HARNESS.harness-new.md`，或在原文件中最小合并。
- 已存在违规先列为历史债，不直接要求全仓清零。
- 新增违规必须从接入当天开始被拦。
- baseline 必须有生成方式和 diff 方式，不能只写一句“历史债以后处理”。
- 红线优先选择最容易失控的边界：旧依赖复活、跨层 import、裸配置、类型逃逸、绕过封装层。

完成标准：

- AI 能在 `docs/workflow.md` 里定位常见任务场景。
- 历史债有清单，不和新增违规混在一起。
- 至少一条核心红线已机械守门。
- 后续 PR 不能新增同类违规。
- Control Map 明确哪些是观察模式、哪些是阻断模式，并有逐步收紧计划。

## 迁移 / 替换项目额外要求

迁移型项目第一条红线必须写旧依赖禁止复活：

```text
R1 被替换的旧依赖禁止任何形式复活
守门：grep / lint 禁 import <legacy>、@<legacy-scope>、window.<legacy>
```

如果旧依赖历史上仍存在：

- 先生成 baseline 清单。
- 新增文件禁止引用旧依赖。
- 每清掉一批历史引用，就收紧 baseline。

## 给 AI 的固定指令

把下面这段交给 AI，即可让它自动接入 harness：

```text
请把 harness 框架落到当前项目。

要求：
1. 先审计当前项目事实：
   - 技术栈
   - 目录结构
   - 构建 / 测试 / lint 命令
   - 现有 README / AGENTS / CLAUDE / GEMINI / CI 配置
   - 已存在的架构约束和常见风险
   - Harnessability：类型反馈、模块边界、测试隔离性、运行日志、关键行为证据

2. 从 harness templates 实例化：
   - AGENTS.md
   - HARNESS.md
   - docs/workflow.md
   - docs/harness-controls.md
   - docs/git-commit-conventions.md
   - 必要的 CLAUDE.md / GEMINI.md / .github/copilot-instructions.md / .cursor/rules 指针
   - scripts/check-redlines.sh

3. 建立 Control Map：
   - 每个重要目标最小登记 Guide、Sensor / 人工确认、失败处置和 Owner
   - 只有执行方式、信任边界或成本不清时，才追加 Guide/Sensor 类型、目标类别和生命周期
   - 区分 Deterministic Gate / Inferential Review Criterion / Human Acceptance Decision
   - 明确 Maintainability / Architecture Fitness / Behaviour 的覆盖边界和不保证项

4. 如果是旧项目：
   - 不要覆盖已有重要文档，冲突时保留旧文件，生成候选版本或做最小合并
   - 红线只写能机械检查的，不要拍脑袋
   - 已存在违规先列为历史债，不要直接让全仓 CI 失败
   - 新增违规必须能被拦
   - baseline 要有生成和 diff 命令，按风险逐步收紧

5. 如果是新项目：
   - 直接按模板生成完整骨架
   - 用项目使命、技术栈、目录规划填充占位符
   - 红线先保守写 3-5 条

6. enforcement 必须接好：
   - 每条 HARNESS 红线都要有 grep / lint / CI 守门
   - 跑 bash scripts/check-redlines.sh
   - 故意写一条违规代码，确认脚本失败
   - 删除违规探针，再确认脚本通过
   - 报错必须能定位问题，并告诉 agent 应读哪份 Guide 或往哪个边界修

7. 行为证据必须独立：
   - 在 SPEC 为关键用例登记 approved fixtures / 既有 contract tests / 外部样例 / 生产回放 / 人工验收之一
   - 当前实现 agent 新生成的测试不能作为唯一验收证据
   - harness-controls 只引用 SPEC 用例锚点，不复制证据内容

8. 最后输出：
   - 生成 / 修改了哪些文件
   - 哪些红线已经机械守门
   - 哪些规则还只是文档约束
   - 哪些历史债需要 baseline
   - 哪些地方需要人工拍板
   - 仅当同类失败至少两次或已有趋势证据时，说明哪些问题进入 Steering Log
```

## AI 输出格式

AI 完成后必须按这个格式收口：

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

Steering（仅达到触发条件时输出）：
- <重复失败模式 / Harness 改动候选 / 复查时间>
```
