# EXP-GATE-001：扫描错误不能当无命中

- failure category：scanner-error-treated-as-no-match。
- 状态：active；Owner：Harness Framework maintainer；目标版本：2.3.0。
- 触发：门禁实现 / 假绿审计；排除：正常业务和 UI / 文案任务。
- 分类：确定性 Gate，不创建新 Skill。
- 事件：本仓 2.2.0 的 grep 脚本将正则 `[` 的错误经 `2>/dev/null || true` 吞掉，仍返回 0。属于控制逃逸；一个高严重度门禁事件足以建 Candidate，同一次回放不计多次事故。
- 原证据：[冻结旧脚本](../fixtures/pre-2.3-check-redlines.sh)，来自 `edf52610c1402950309bb941de136deae899051e:examples/node-orders-api/scripts/check-redlines.sh`。
- 正式事实源：[当前模板](../../../templates/enforcement/scripts/check-redlines.sh)、[baseline checker](../../../scripts/check-baseline.py)。条目不复制规则实现。
- Eval：`python3 examples/experience-loop/replay.py`；坏正则旧版 PASS / 新版 ERROR；合法输入 PASS；违规输入 FAIL；命中 / 非命中路由验证。更多错误与规则探针见 `scripts/test-enforcement.py`。
- 授权：用户本轮明确请求“请给我做一次进化，rcp”，覆盖本框架维护与 RCP；不伪造额外的人类批准记录。
- 模型有 / 无 Skill A/B：not-run。此回放只证明 Gate 行为，不证明模型收益。
- 回滚 / 复查：误报、扫描器替换、规则语法 / 输入范围变化时复评；回滚不得恢复吞错。替代或退役时退出默认召回，保留此证据与替代 ID。

评测命令、状态和正式版本必须匹配；发布到其他项目仍按该项目授权与风险维护。

本轮实际进度：审计发现并形成候选 → 原失败及反例评测通过 → 按既有维护授权纳入 2.3；未发生退役，退役仅在 replay 的明确模拟数据中验证。
