# node-orders-api · workflow §1 场景表（填好版样例）

> `workflow.template.md §1` 填实后的样子。后端服务只需 5 行场景，不必凑满 8 行。

| # | 场景 | 先读哪份 | 必守红线（HARNESS §8） | 产出落在哪 | DoD |
| --- | --- | --- | --- | --- | --- |
| 1 | **新增 / 改业务用例（如「下单」「退款」）** | `SPEC.md` 对应用例 + `data-contracts.md` | R1 domain 禁 prisma、R3 禁 as any、R7 覆盖率 | `src/domain/**` 纯函数 + `src/services/**` + 单测 | 用例验收 + service/domain 覆盖率 ≥ 80% |
| 2 | **加 / 改 API 路由** | `openapi.yaml` + `SPEC.md` | R4 禁裸 process.env、R6 路由禁裸 SQL | `src/routes/**`，不写业务逻辑 | 契约测试通过 + OpenAPI 同步更新 |
| 3 | **改 DB schema / 迁移** | `prisma/schema.prisma` + 相关 ADR | R1（只有 `db/` 能碰 prisma） | `prisma/migrations/**` + `src/db/**` | 迁移可回滚 + 种子数据更新 |
| 4 | **从旧单体迁一块能力过来** | `migration-ledger.md`（解绑账目） | R2 旧单体禁复活（迁完即断 import） | `src/<新模块>/**` + 在账目里勾掉对应行 | 主仓 grep 不到 `@acme/monolith` 该模块引用 |
| 5 | **加 / 改 / 删依赖** | `deps.md` + `adr/README.md` | R2 禁旧单体、不引同类第二套 ORM | `package.json`（lockfile 同步）+ 新 ADR | `pnpm install --frozen-lockfile` 无漂移 + ADR Accepted |

## 按需载入（节选）

| 会话目的 | 必载 | 按需 |
| --- | --- | --- |
| 写新用例 | `SPEC.md` 对应用例 | `openapi.yaml`（若动接口） |
| 迁旧单体能力 | `migration-ledger.md` | 旧单体对应模块源码 |
| 改依赖 | `deps.md` | 上一篇相关 ADR |
