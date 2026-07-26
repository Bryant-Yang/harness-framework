# node-orders-api · Harness Controls（填好版节选）

<!-- harness:control-map=minimum -->
<!-- harness:behaviour-evidence=spec-reference-only -->
<!-- harness:experience-trigger=repeat-2-or-high-severity-1 -->
<!-- harness:context-routing=progressive-and-probed -->
<!-- harness:experience-promotion=candidate-first -->
<!-- harness:runner-consumption=optional -->

> 展示同一个目标如何同时拥有 Guide、Sensor / 人工确认、失败处置和责任边界。

## 覆盖边界

| 调节目标 | 当前覆盖 | 证据索引（不复制内容） | 明确不保证什么 |
| --- | --- | --- | --- |
| Maintainability | 成熟 | typecheck、lint、红线 grep、单测 | 不能可靠判断是否过度设计 |
| Architecture Fitness | 部分 | domain 禁 Prisma、路由禁裸 SQL | 尚无真实性能与可观测性 Sensor |
| Behaviour | 部分 | [`SPEC.md#uc-ord-001-创建订单`](SPEC.md#uc-ord-001-创建订单) | AI 新写的测试不能单独证明业务正确 |

## Control Map

| ID | 目标 | Guide | Sensor / 人工确认 | 失败处置 | Owner |
| --- | --- | --- | --- | --- | --- |
| C1 | domain 保持纯业务 | `AGENTS.md` + 分层说明 | R1 grep + eslint import rule | agent 修复并复验 | Tech Lead |
| C2 | 旧单体不复活 | 迁移账目 + R2 | baseline diff + R2 grep | 阻断新增引用 | Migration Owner |
| C3 | 下单行为符合业务 | `SPEC.md` UC-ORD-001 | contract tests + 产品验收 | 修实现或重新澄清 SPEC | Product Owner |
| C4 | 不引入无必要抽象 | 北极星原则 | PR architecture review | 给出证据，由 reviewer 裁决 | Reviewer |

## Behaviour Evidence 引用

| 用例 / 风险 | SPEC 证据位置 | 相关 Control |
| --- | --- | --- |
| 创建订单 | [`SPEC.md#uc-ord-001-创建订单`](SPEC.md#uc-ord-001-创建订单) | C3 |

## Legacy baseline（R2）

```bash
# 接入日生成一次并纳入版本控制
{ rg -n '@acme/monolith' src || true; } | sed -E 's/^([^:]+):[0-9]+:/\1:/' | sort > docs/baselines/R2-legacy-monolith.txt

# CI 重新生成当前命中；显式检查相对基线的新增引用
{ rg -n '@acme/monolith' src || true; } | sed -E 's/^([^:]+):[0-9]+:/\1:/' | sort > /tmp/R2-current.txt
new_hits="$(comm -13 docs/baselines/R2-legacy-monolith.txt /tmp/R2-current.txt)"
[ -z "$new_hits" ] || { printf 'R2 新增旧单体引用：\n%s\n' "$new_hits"; exit 1; }
```

## Context Routing Sensor

`AGENTS.md → workflow-scenes.md` 必须命中一个场景，并能找到目标层契约与 `SPEC.md` 关闭证据。若任务只改依赖，不把整份 SPEC 和全部 ADR 装入上下文。

## Experience Promotion

> 不在实例化时填写空记录；以下 Candidate 由两次同类失败触发，尚未批准前不改正式 Skill。

| 日期 | Evidence / 触发 | 分类与 Candidate | 适用 / 不适用 | Eval | Owner / 发布与回滚 |
| --- | --- | --- | --- | --- | --- |
| 2026-06-06 | 两次在 route 中拼 SQL；关联 diff #118 / #126 | 可机械拒绝模式 → Candidate R6 Gate | 适用 `src/routes/**`；不适用 repository migration | 原失败回放失败、repository 反例通过、场景路由命中 | Tech Lead；批准后发布，误报则回滚规则 |

## Runner Consumption Contract

本样例没有 Codex Goal、Mission Driver 或外部 runner，因此不创建 runner 配置或空表。
