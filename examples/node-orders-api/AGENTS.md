# AGENTS.md — node-orders-api Agent 协作契约

> 作者：Bryant Yang　最近更新：2026-06-06
>
> 这是 `templates/AGENTS.template.md` 的填好版样例，用来展示 harness 落到一个
> Node + TypeScript 后端服务时应该长什么样。

## 1. 项目一句话

Node 20 + TypeScript + Fastify + Postgres（Prisma）的订单服务。
**使命：把订单域从 `legacy-monolith` 拆成独立服务，终态主仓不再 import `@acme/monolith`。**

## 2. 必读清单

| 优先级 | 文件 | 用途 |
| --- | --- | --- |
| P0 | `README.md` | 样例说明与项目设定 |
| P0 | `HARNESS-redlines.md` | 填好版红线三列表 |
| P0 | `workflow-scenes.md` | 填好版场景表 |
| P0 | `scripts/check-redlines.sh` | 可执行红线 grep 守门 |

最小入场顺序：`README.md` → `workflow-scenes.md` 定位场景 → `HARNESS-redlines.md` 红线 → `scripts/check-redlines.sh` 自查。

## 3. 不可破的硬约束

1. `domain/` 是纯业务层，禁止 import `prisma` / `@prisma/client`。
2. 被拆分的旧单体禁止复活，任何位置禁止 import `@acme/monolith`。
3. 禁止类型逃逸：`as any` / `as unknown as`。
4. 配置必须走 `config/env.ts`，禁止业务代码裸读 `process.env.X`。
5. 日志必须走统一 `logger`，禁止 `console.log` / `console.debug`。
6. 路由层禁止裸 SQL 字符串，必须经 service / repository。

## 4. 工作动作

- 写功能前先在 `workflow-scenes.md` 找到对应场景。
- 改动后先跑 `bash scripts/check-redlines.sh`。
- 新代码必须补单测；覆盖率红线由 CI `vitest run --coverage` 守。
- `git add` 必须显式列文件，禁止 `git add .` / `git add -A`。
- commit message 必须走 Conventional Commits。

## 5. 行为风格

- 中文回复，必要术语保留英文。
- 只动任务需要的文件，不顺手重构邻居代码。
- 对契约有疑问时先停下说明冲突，不用猜测合并两套规则。
