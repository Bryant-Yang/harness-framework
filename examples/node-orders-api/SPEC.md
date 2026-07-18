# node-orders-api · Behaviour Evidence（填好版节选）

<!-- harness:behaviour-evidence=canonical-source -->

> `SPEC.md` 是关键 Behaviour 独立证据与人工验收边界的唯一事实源；`harness-controls.md` 只引用本用例。

## UC-ORD-001 创建订单

- **角色 / 触发**：已登录客户提交有效购物车。
- **前置条件**：商品可售，价格快照已确认，请求带幂等键。
- **主流程**：校验购物车 → 固化价格 → 创建订单 → 返回订单编号。
- **异常分支**：库存不足返回明确业务错误；重复幂等键返回首次创建结果。
- **验收（可测）**：API contract tests 覆盖成功、库存不足与幂等重放。
- **独立证据来源**：产品负责人批准的订单 fixtures `orders-v1`，由 contract tests 读取。
- **人工验收边界**：价格展示、错误文案和取消政策仍由 Product Owner 验收。
- **里程碑**：M1。
