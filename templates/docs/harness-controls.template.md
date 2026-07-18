# <PROJECT> Harness Controls

<!-- harness:control-map=minimum -->
<!-- harness:behaviour-evidence=spec-reference-only -->
<!-- harness:steering-trigger=min-occurrences-2 -->

> Framework version：2.0.1　项目实例版本：<YYYY-MM-DD / commit>
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

> `SPEC.md` 是关键 Behaviour 独立证据与人工验收边界的唯一事实源。本文只保存引用，不复制证据内容。

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

## 6. Steering Log

> 同类失败至少出现两次，或已有趋势证据时才建立记录；初始化时本节只保留触发规则，不创建表格。触发后再记录：日期、重复失败证据、根因分类、Harness 改动、负向验证、Owner 与复查日。

## 7. Baseline 与模板升级

- **Legacy baseline**：<基线文件 / 生成命令 / 只拦新增的比较命令>。参考形态：`{ rg -n '<模式>' src || true; } | sed -E 's/^([^:]+):[0-9]+:/\1:/' | sort > docs/baselines/R1.txt` 生成去行号基线；CI 用同一命令生成当前命中，再执行 `new_hits="$(comm -13 <baseline> <current>)"; [ -z "$new_hits" ] || { printf '%s\n' "$new_hits"; exit 1; }`。`comm` 自身不会因有输出而失败，所以必须显式判断；`|| true` 允许零命中，去掉行号可避免无关代码移动制造假新增。
- **模板来源**：Harness Framework `2.0.1`，来源 commit `<sha>`。
- **本地差异**：<哪些是项目事实，升级时不得自动覆盖>。
- **升级策略**：先看上游 diff，区分 bug fix / optional control / breaking policy，再人工合并并重跑负向验证。
