# node-orders-api · HARNESS §8 红线（填好版样例）

> 这是 `HARNESS.template.md §8` 填实后的样子。8 条红线，**每条都有可执行守门命令**，
> 与 `scripts/check-redlines.sh` 和 `eslint.config.ts` 一一对应。

| # | 红线 | 守门命令 | 谁拦 |
| --- | --- | --- | --- |
| R1 | `domain/` 是纯业务，禁止 import `prisma` / `@prisma/client`（DB 只能从 `db/` 进） | eslint `no-restricted-imports`（`domain/**` 禁 prisma）；`check "R1" "domain 禁 prisma" "from ['\"]@?prisma" src/domain` | grep + lint |
| R2 | 被拆分的旧单体禁止复活：禁止 import `@acme/monolith` | eslint regex 禁 `^@acme/monolith`；`check "R2" "旧单体禁复活" "@acme/monolith" src` | grep + lint |
| R3 | 禁止类型逃逸 `as any` / `as unknown as` | `check "R3" "禁 as any" '\bas any\b\|as unknown as' src` + eslint `no-explicit-any` | grep + lint |
| R4 | 禁止裸 `process.env.X`，配置必须走 `config/env.ts`（集中校验） | `check "R4" "禁裸 process.env" "process\.env\." src/services src/domain src/routes` | grep |
| R5 | 禁止 `console.log`，日志走 `logger`（生产可控级别） | `check "R5" "禁 console.log" "console\.(log\|debug)" src` | grep |
| R6 | 路由层禁止直接写 SQL 字符串，必须经 service + repository | `check "R6" "路由禁裸 SQL" "(SELECT\|INSERT\|UPDATE\|DELETE)\s" src/routes` | grep |
| R7 | 新代码无单测不进 main（service/domain 覆盖率 ≥ 80%） | CI `vitest run --coverage` + 阈值 | CI |
| R8 | commit 必走 Conventional Commits | `commitlint` type-enum | commit-msg 钩子 |

> 注意被砍掉的伪红线：原本想写「代码要可读」「函数别太长」——
> **写不出 grep/lint 命令**，所以降级到北极星「反 God-Class」原则，不进红线表。
> 文件行数确实想守的话，用 `check "R-len" ... $(find ... -exec wc -l)` 脚本，那才算红线。
