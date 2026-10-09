# 决策记录索引（Architecture Decision Records）

> 作者：<AUTHOR>　最近更新：<YYYY-MM-DD>
>
> 每个重大决定写一篇 ADR。模板见 [`_template.md`](_template.md)。
>
> ADR 正文一经合入，**只能通过新 ADR（标记 `Supersedes ADR-NNNN`）来修订；不允许直接编辑旧 ADR 正文**。本索引可以更新状态与交叉引用；只有同一决策领域的 Accepted ADR 且明确 `Supersedes` 旧决策时才替代旧决策；日期较新不自动胜出，ADR 不覆盖业务规格。证据无法消解实质冲突时暂停依赖分支并说明。

## 已落地

| 编号 | 标题 | 状态 |
| --- | --- | --- |
| ADR-0001 | <标题> | Accepted |
| ADR-0002 | <标题> | Accepted |

## 启动期必落地清单

> 列出主线开发启动前必须全部 Accepted 的 ADR。

| 编号 | 标题 | 状态 |
| --- | --- | --- |
| ADR-000X | <关键决策> | Pending |

## 写作守则

1. 文件名 `NNNN-<kebab-case-标题>.md`，编号四位。
2. 提交 PR 时附带模板填空，缺项不允许合入。
3. 决策被推翻时**新建** `Supersedes` 关系的 ADR；旧 ADR 正文不改，只在本索引的状态列标记 `Superseded by ADR-NNNN`。
4. 同步更新本索引的状态列与标题。

## 何时该写一份 ADR

- 引入或剔除一个直接依赖；
- 改变跨模块约定（命名空间、接口契约、数据流方向）；
- 调整性能预算或测试分层；
- 决定一项与 [`../../HARNESS.md`](../../HARNESS.md) 红线冲突或例外的临时方案；
- 任何让「未来 6 个月内的同事会问『为啥这么干』」的决定。
