# AGENTS.md — node-orders-api Agent 协作契约

<!-- harness:controls-read-policy=on-demand -->
<!-- harness:context-routing=progressive-and-probed -->

> 作者：Bryant Yang　最近更新：2026-06-06
>
> 这是 `templates/AGENTS.template.md` 的填好版样例，用来展示 harness 落到一个
> Node + TypeScript 后端服务时应该长什么样。

## 1. 项目一句话

Node 20 + TypeScript + Fastify + Postgres（Prisma）的订单服务。
**使命：把订单域从 `legacy-monolith` 拆成独立服务，终态主仓不再 import `@acme/monolith`。**

## 2. 上下文路由表

| 优先级 | 文件 | 用途 |
| --- | --- | --- |
| Always-on | `README.md` | 样例说明与项目设定 |
| Always-on | `workflow-scenes.md` | 场景与 Context Routing |
| Always-on | `HARNESS-redlines.md` | 全局红线三列表 |
| Task-loaded | `SPEC.md` | 命中业务场景时读取 Behaviour Evidence |
| Task-loaded | `harness-controls.md` | 软约束、人工边界、重复失败或 runner 相关时读取 |
| Phase-loaded | `scripts/check-redlines.sh` | 实现 / 提交阶段执行红线守门 |

最小入场顺序：`README.md` → `workflow-scenes.md` 定位场景 → `HARNESS-redlines.md` 红线 → `scripts/check-redlines.sh` 自查。

Routing Probe：确认场景已命中、改动层有对应契约、`SPEC.md` 的关闭证据锚点可达。在平台规则与用户当前指令之下，项目事实优先于 Skill 和临时 memory；冲突时直接报告。

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
- 单次普通失败只修当前任务；重复至少两次或一次高严重度逃逸时，才在 `harness-controls.md` 创建 Candidate，并经回放、反例与 Owner 批准后晋级。
