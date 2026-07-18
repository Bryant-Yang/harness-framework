# <PROJECT> Harness Controls

> Framework version：2.0.0　项目实例版本：<YYYY-MM-DD / commit>
>
> 本文把重要目标映射为 Guide、Sensor、执行时机和责任人。它不替代 `HARNESS.md`、`SPEC.md`
> 或具体工具配置，只负责证明控制闭环是否完整。

## 1. 覆盖边界

| 调节目标 | 当前覆盖 | 主要证据 | 明确不保证什么 |
| --- | --- | --- | --- |
| Maintainability | <成熟 / 部分 / 空白> | <lint / typecheck / tests / review> | <例如：不能可靠判断是否过度设计> |
| Architecture Fitness | <成熟 / 部分 / 空白> | <结构测试 / 性能预算 / 可观测性检查> | <例如：未覆盖生产流量下的性能> |
| Behaviour | <成熟 / 部分 / 空白> | <contract tests / approved fixtures / 人工验收> | <例如：AI 自生成测试不是独立需求证据> |

## 2. Control Map

> 重要目标至少有一条检测或明确的人类确认路径。能机械判断的不要交给 LLM；无法可靠机械判断的不要伪装成硬门禁。

| ID | 目标 | Guide（行动前） | Guide 类型 | Sensor（行动后） | Sensor 类型 | 生命周期 | 失败处置 | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | <目标> | <文档 / Skill / 脚本> | Computational / Inferential | <测试 / lint / review / 人工验收> | Computational / Inferential / Human | 本地 / 提交 / 集成后 / 持续 / 运行时 | <自修 / 阻断 / 建单 / 人工裁决> | <责任人> |

## 3. 约束等级

| ID | 等级 | 判据 | 允许的处置 |
| --- | --- | --- | --- |
| <R1 / C?> | Deterministic Gate | <可稳定机械判断，低误报> | 违反必拦；修复后复验 |
| <S?> | Inferential Review Criterion | <需要语义或权衡> | 报告证据和建议，不伪装成确定事实 |
| <A?> | Human Acceptance Decision | <业务意图、风险或责任> | 由明确责任人签收；agent 不代签 |

## 4. Behaviour Evidence

> 当前实现 agent 自己生成的测试不能成为唯一验收证据。

| 用例 / 风险 | 独立证据来源 | 谁批准 | 自动检查 | 人工验证 | 最近验证 |
| --- | --- | --- | --- | --- | --- |
| <UC-...> | approved fixture / contract test / 外部样例 / 生产回放 | <人> | <命令> | <步骤> | <日期> |

## 5. 反馈生命周期

| 阶段 | 预算 | 必跑 Sensors | 反馈给谁 | 失败后 |
| --- | --- | --- | --- | --- |
| Agent 本地循环 | 秒级 | <相关 lint / typecheck / tests> | 当前 agent | 修复并复验 |
| 提交门禁 | 分钟级 | <redlines / 全量 lint / 相关测试> | 提交者 | 阻断提交 |
| 人工 Review | 按风险 | <语义 / spec / 风险检查> | Reviewer | 修改或明确接受风险 |
| 集成后 | 较昂贵 | <全量测试 / mutation / 架构检查> | 维护队列 | 建单或回滚 |
| 持续健康 / 运行时 | 周期性 | <漂移 / SLO / 日志异常> | Owner | 带证据提出改进，不直接改生产 |

## 6. Steering Log

> 同类问题重复出现时，不只修当前代码；判断缺 Guide、缺 Sensor、二者冲突，还是目标本身不清楚。

| 日期 | 重复失败模式与证据 | 根因分类 | Harness 改动 | 负向验证 | Owner / 复查日 |
| --- | --- | --- | --- | --- | --- |
| <YYYY-MM-DD> | <至少两个实例或趋势证据> | 缺 Guide / 缺 Sensor / 冲突 / 目标不清 | <新增、修改或删除的控制> | <如何证明会触发且可修复> | <人 / 日期> |

## 7. Baseline 与模板升级

- **Legacy baseline**：<基线文件 / 生成命令 / 只拦新增的比较命令>。参考形态：`{ rg -n '<模式>' src || true; } | sed -E 's/^([^:]+):[0-9]+:/\1:/' | sort > docs/baselines/R1.txt` 生成去行号基线；CI 用同一命令生成当前命中，再执行 `new_hits="$(comm -13 <baseline> <current>)"; [ -z "$new_hits" ] || { printf '%s\n' "$new_hits"; exit 1; }`。`comm` 自身不会因有输出而失败，所以必须显式判断；`|| true` 允许零命中，去掉行号可避免无关代码移动制造假新增。
- **模板来源**：Harness Framework `2.0.0`，来源 commit `<sha>`。
- **本地差异**：<哪些是项目事实，升级时不得自动覆盖>。
- **升级策略**：先看上游 diff，区分 bug fix / optional control / breaking policy，再人工合并并重跑负向验证。
