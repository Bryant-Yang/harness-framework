# node-orders-api · Harness Controls（填好版节选）

<!-- harness:control-map=minimum -->
<!-- harness:behaviour-evidence=spec-reference-only -->
<!-- harness:steering-trigger=min-occurrences-2 -->

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

## Steering Log

> 不在实例化时填写空记录；以下条目由两次同类失败触发。

| 日期 | 重复失败模式与证据 | 根因分类 | Harness 改动 | 负向验证 | Owner / 复查日 |
| --- | --- | --- | --- | --- | --- |
| 2026-06-06 | 两次在 route 中拼 SQL | Guide 有、Sensor 缺 | 新增 R6 grep，并把报错指向 repository 层 | 在 `src/routes` 放 `SELECT` 探针，脚本必须失败 | Tech Lead / 2026-07-06 |
