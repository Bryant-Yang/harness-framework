# node-orders-api · HARNESS §8（假想项目示范）

这是工程契约的写作示例。R1–R6 已实现有限文本 smoke，检查对应字面模式；它们不证明所有语法形式或业务语义被拦截。R7 / R8 只有待接线要求，不能算生效门禁。

| # | 目标 | 当前命令 / 状态 | 检测边界与补充 |
| --- | --- | --- | --- |
| R1 | domain 不引用 Prisma | `check "R1"`，已实现文本 smoke | 单行 `from` 模式；多行 / 动态 import 需 AST |
| R2 | 禁止旧单体 `@acme/monolith` | `check "R2"`，已实现文本 smoke | 固定字面包名；运行时间接依赖另查 |
| R3 | 禁止类型逃逸 | `check "R3"`，已实现文本 smoke | 单行断言；多行 `any` 需 TypeScript lint |
| R4 | 配置经统一入口 | `check "R4"`，已实现文本 smoke | `process.env.`；计算属性 / 别名需 AST |
| R5 | 日志经 logger | `check "R5"`，已实现文本 smoke | 点号 `console.log/debug`；计算属性需 AST |
| R6 | SQL 经 service / repository | `check "R6"`，已实现文本 smoke | 大写 SQL 文本；小写 / 拼接 / 注释存在漏检或误报，不是语义保证 |
| R7 | 关键模块覆盖率 ≥ 80% | 未实现：项目 CI 接 coverage 阈值 | 覆盖率不证明每段新代码有独立验收 |
| R8 | Conventional Commits | 未实现：项目接 commitlint / CI | 框架 fixture 已测试 commitlint，不代表本假想项目 CI 已配置 |

运行 `bash scripts/check-redlines.sh`；返回 0 = 当前配置文本检查通过，1 = 模式命中，2 = 配置 / 扫描错误。两类非零状态都阻断。无需测试的低风险文字修改和语义判断不提升为硬门禁。
