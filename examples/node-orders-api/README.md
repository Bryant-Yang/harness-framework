# 样例：node-orders-api —— 一个填好的 harness 长什么样

> 这是一个**字段填好的异构样例**（Node + TS 后端订单服务），不是 Cesium 前端。
> 目的：让你从「空模板」跳到「成品」时有个参照——尤其是最难的**红线三列表 + 配套守门脚本**。
>
> 它不是要跑起来的真项目，只展示 harness 各机制**填实**后的形态。

## 假想项目设定

- **是什么**：订单服务，REST API。Node 20 + TypeScript + Fastify + Postgres（Prisma）。
- **使命**：从单体 `legacy-monolith` 里把订单域拆成独立服务，**终态主仓不再 import `@acme/monolith`**。
  （注意这和 dw_gis3d「替代 HT」是同构的：替换型项目，红线要守「旧依赖不复活」。）
- **分层**：`routes/ → services/ → domain/ → db/`，`domain/` 是纯函数，禁止 import `prisma`。

## 看点：红线如何从「声明」变成「闸门」

下面 `HARNESS-redlines.md` 是填好的 §8 三列表，`scripts/check-redlines.sh` 是它对应的可执行守门。
R1–R6 有可运行的文本 smoke，R7 / R8 仅示范项目 CI / commitlint 接线，不能宣称本样例已实现全部红线。多行 import、动态 import、计算属性、大小写变体可能绕过 grep；语义保证必须另接 AST / lint。框架的 TypeScript 骨架及真实 toolchain probes 位于 `templates/enforcement/ts/` 和 `tests/enforcement/ts/`，同样明确静态 import 的覆盖边界。

| 文件 | 对应模板 |
| --- | --- |
| `AGENTS.md` | `templates/AGENTS.template.md` 填好版 |
| `HARNESS-redlines.md` | `templates/HARNESS.template.md §8` 填好版 |
| `scripts/check-redlines.sh` | `templates/enforcement/scripts/check-redlines.sh` 填好版 |
| `workflow-scenes.md` | `templates/docs/workflow.template.md §1` 填好版 |
| `harness-controls.md` | `templates/docs/harness-controls.template.md` 填好版节选 |
| `SPEC.md` | Behaviour Evidence 唯一事实源的填好版节选 |

## 一句话对照

dw_gis3d 守「禁止 `import 'cesium'`/`ht.*`」，这个样例守「禁止 `import 'prisma'` 进 domain / 禁止 `@acme/monolith` 复活」。
**机制完全相同，红线内容不同**——这正是框架可复用的证明。

`harness-controls.md` 再向上补一层：它说明这些闸门保护什么目标、行动前读什么 Guide、失败后如何处置、谁负责验收，并只引用 `SPEC.md` 的 Behaviour Evidence；上下文按场景加载，重复失败或高严重度逃逸先形成 Candidate，经回放、反例与 Owner 批准后才晋级。

实际自证：`python3 scripts/test-enforcement.py --with-toolchains`（从框架根目录，先安装 fixture 的锁定依赖）。业务 fixtures / contract tests 为假想内容，未运行。真实经验回放见 [experience-loop](../experience-loop/README.md)。
