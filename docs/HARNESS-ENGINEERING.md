# Harness Engineering 上位模型

> Harness Framework 2.0.0 将 Birgitta Böckeler 在 Martin Fowler 网站发表的
> [Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html)
> 中提出的控制系统视角，落成一套轻量、可实例化的工程契约方法。
>
> 本文是方法说明，不是工具清单。框架仍坚持 docs-as-contract，不演变成重型平台。

## 1. 边界：我们建设的是用户侧 Outer Harness

模型与 coding agent 产品自身已经带有 system prompt、代码检索、工具调用和编排等内层 harness。
本框架关注更外层的用户 harness：团队针对自己的代码库、业务边界和风险建立的 Guides、Sensors
与治理流程。

```text
用户 Harness（本框架）
└── Coding Agent Harness（工具厂商提供）
    └── Model
```

## 2. Harness 不是规则包，而是控制闭环

```text
Guide 预先引导
  → Agent 产生变更
  → Sensor 检测偏差
  → Agent 自我修正
  → Sensor 再验证
  → Human Steering 根据重复失败升级 Guide / Sensor
```

- **Guides（feedforward）**：行动前提高首次做对的概率。
- **Sensors（feedback）**：行动后提供可定位、可修复、可复验的信号。
- **Self-correction**：当前变更内的修正循环。
- **Human Steering**：观察重复失败，持续校准整个 harness。

只有 Guide，没有 Sensor，无法证明规则生效；只有 Sensor，没有 Guide，agent 会反复犯同一种错误。

## 3. 四个正交维度

每项重要控制都应能回答四个问题。

| 维度 | 选项 | 要回答的问题 |
| --- | --- | --- |
| 方向 | Feedforward / Feedback | 它在行动前引导，还是行动后检测？ |
| 执行 | Computational / Inferential / Human | 它是确定性执行、模型判断，还是人类裁决？ |
| 目标 | Maintainability / Architecture Fitness / Behaviour | 它调节哪类质量？ |
| 时机 | 本地 / 提交门禁 / 集成后 / 持续健康 / 运行时 | 它在何时运行，成本与范围多大？ |

### 3.1 控制矩阵

| | Feedforward 前馈 | Feedback 反馈 |
| --- | --- | --- |
| Computational 计算型 | LSP、脚本、codemod、生成器 | 测试、lint、类型检查、结构分析 |
| Inferential 推理型 | AGENTS.md、Skills、原则、How-to | AI review、架构 review、LLM judge |

原则：**能计算的不要推理；无法可靠形式化的，不要伪装成确定性门禁。**

### 3.2 三种约束等级

| 等级 | 含义 | 处理方式 |
| --- | --- | --- |
| Deterministic Gate | 可以稳定、低误报地机械判断 | 违反必拦，并提供可修复报错 |
| Inferential Review Criterion | 需要语义和权衡判断 | 给出证据与建议，由 review 流程处理 |
| Human Acceptance Decision | 涉及业务意图、风险与责任 | 必须由明确责任人验收或批准 |

“写不出 grep 就不是红线”仍然成立，但不代表它不重要；它可能属于推理型 review criterion 或人类验收。

## 4. 三类调节目标与信任边界

### Maintainability Harness

当前最成熟。重复代码、复杂度、覆盖率、依赖方向和风格适合确定性检测；语义重复、暴力修复与过度设计只能概率性判断。

### Architecture Fitness Harness

把承重架构属性变成持续 fitness functions，例如模块边界、性能预算、可观察性和错误处理。ADR 解释“为什么”，Sensor 负责持续检查“是否仍成立”。

### Behaviour Harness

当前最薄弱。Agent 解释需求、实现功能、再生成测试证明自己正确，不是独立证据。关键行为至少需要一种来源独立的验收依据：

- 人工批准的 fixtures；
- 既有 contract tests；
- 外部验收样例；
- 生产回放数据；
- 关键路径人工测试。

覆盖率和 mutation score 能评价测试强度，不能单独证明需求理解正确。

## 5. 反馈生命周期

```text
本地循环 → 提交门禁 → 人工 Review → 集成后检查 → 持续漂移 / 运行时反馈
  快、局部、便宜                                  慢、全局、昂贵
```

- 秒级确定性检查尽量左移到 agent 每轮修改之后。
- 全库架构分析、mutation testing、深度语义 review 放在更晚阶段。
- Dead code、依赖风险和覆盖质量属于持续漂移 Sensor。
- SLO、错误率、延迟和日志异常属于运行时 Sensor。
- 左移不是把所有生产验证搬到本地；执行时机必须匹配信号真实性与成本。

## 6. Harnessability

Harnessability 是代码库“能否被清晰引导、可靠检测、低歧义修正”的程度。审计至少检查：

- 类型和编译反馈是否可靠；
- 模块边界是否可表达、可检查；
- 测试是否可隔离、可重复；
- 关键行为是否有独立验收证据；
- 运行日志是否足以诊断；
- 历史债是否能建立 baseline，只拦新增。

Legacy 项目建议按 `观察 → baseline → 只拦新增 → 逐步收紧` 演进，不追求第一天全绿。

## 7. Harness Templates：结构 × 技术栈 × 控制

成熟组织常见的服务拓扑可以沉淀为 Harness Template：不仅提供代码骨架，还把结构、技术栈、Guides 和 Sensors 一起打包。例如“Node 数据看板”“JVM CRUD 服务”“Go 事件处理器”应拥有不同的边界、门禁和反馈预算。

模板不是强迫所有项目一致，而是给 80% 常见拓扑一个经过验证的起点。实例化后必须记录来源版本、本地事实差异和升级策略；上游更新不能自动覆盖项目决策。

```text
Structure + Tech Stack + Guides + Sensors → Harness Template → Project Instance
```

## 8. Harness 也需要被治理

- Guide 与 Sensor 必须保持一致，避免一个要求 A、另一个奖励 B。
- Sensor 从不触发，既可能代表高质量，也可能代表检测失效；必须用负向探针校准。
- 指标会产生 Goodhart 风险，门禁通过不等于系统更好。
- 模板实例会与上游漂移，必须记录版本并走人工审查的升级协议。
- 高影响 harness 变更由 agent 提案、提供失败样例和影响面，由人批准。
- Harness 的目标不是消灭人，而是把人的注意力留给业务意图、例外、风险和责任判断。

落地载体见 [`../templates/docs/harness-controls.template.md`](../templates/docs/harness-controls.template.md)。
