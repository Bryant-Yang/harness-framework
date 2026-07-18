# 实例化检查清单 —— 把框架落到新工程

> 跟着勾。全部勾完，新工程就有了一套自洽、可 grep、可驳回的工程契约。

## 一、拷贝与改名

- [ ] 若让 AI 自动接入，先把 [`AI-ADOPTION-PROTOCOL.md`](AI-ADOPTION-PROTOCOL.md) 里的固定指令交给 agent 执行
- [ ] 把 `templates/` 下全部文件拷到新工程根目录
- [ ] `AGENTS.template.md` → `AGENTS.md`
- [ ] `HARNESS.template.md` → `HARNESS.md`
- [ ] `PROJECT-README.template.md` → `README.md`
- [ ] `docs/SPEC.template.md` → `docs/SPEC.md`
- [ ] `docs/workflow.template.md` → `docs/workflow.md`
- [ ] `docs/harness-controls.template.md` → `docs/harness-controls.md`
- [ ] `docs/git-commit-conventions.template.md` → `docs/git-commit-conventions.md`
- [ ] `docs/adr/README.template.md` → `docs/adr/README.md`（`_template.md` 保持原名）
- [ ] `docs/decisions/README.template.md` → `docs/decisions/README.md`

## 二、占位符替换（全局搜替）

- [ ] `<PROJECT>` → 项目名
- [ ] `<AUTHOR>` → 作者署名
- [ ] `<YYYY-MM-DD>` → 当天日期
- [ ] `<MISSION>` → 使命一句话
- [ ] `<语言>` → 团队工作语言
- [ ] `<CI_CMD>` → 真实 CI 命令串
- [ ] `docs/harness-controls.md` 记录 Harness Framework 版本、来源 commit 与本地差异
- [ ] 技术栈表、目录树、分层箭头按项目实情画

## 三、长出红线（最关键一步）

- [ ] HARNESS §8 红线逐条改写成**你项目里能 grep 的约束**
- [ ] 每条红线确认：谁来查、用什么命令查？查不了的降级到北极星或普通规范
- [ ] AGENTS §3「不可破硬约束」与 HARNESS §8 编号对齐
- [ ] workflow §2「红线速记」与 HARNESS §8 编号严格对齐

## 四、场景表落地

- [ ] workflow §1 把示例 8 行改成你项目的真实场景（小项目 3–4 行即可）
- [ ] 每行 5 列（先读哪份 / 守哪条红线 / 产出在哪 / DoD）都答全
- [ ] workflow §3「按需载入」与 §1 场景对应

## 五、建立控制闭环

- [ ] 在 `docs/harness-controls.md` 写清 Maintainability / Architecture Fitness / Behaviour 的覆盖边界
- [ ] 每个重要目标分别登记 Guide 类型与 Sensor 类型，并填写生命周期、失败处置和 Owner
- [ ] 约束分成 Deterministic Gate / Inferential Review Criterion / Human Acceptance Decision
- [ ] 关键 Behaviour 至少有一种独立证据，不能只靠当前 agent 自己生成的测试
- [ ] Legacy 项目的 baseline 有生成命令与只拦新增的 diff 命令
- [ ] Steering Log 已指定 Owner 与复查节奏

## 六、清理示例

- [ ] 删掉所有 `> 示例（dw_gis3d）：` 引用块
- [ ] 删掉所有 `<!-- 占位符清单 -->` 注释（或保留作维护提示，自行决定）

## 七、接线（让契约真正生效，而不只是文档）

### 7.1 多工具入口指针（机制 0，agent-first 关键）

> 按团队实际用的工具放对应指针。原生读 `AGENTS.md` 的工具(Codex/Cursor/Copilot/Windsurf 等)一个都不用放。

- [ ] 用 Claude Code → 拷 `CLAUDE.md`（含 `@AGENTS.md`）
- [ ] 用 Gemini CLI → 拷 `GEMINI.md`（含 `@AGENTS.md`）
- [ ] 用 Google 反重力 Antigravity → 拷 `GEMINI.md`（防被空覆盖；它也原生读 AGENTS.md）
- [ ] 用旧版 Cursor / 偏好 `.cursor/rules` 优先级 → 拷 `.cursor/rules/000-agents.mdc`
- [ ] 偏好 `.github/copilot-instructions.md` → 拷该文件
- [ ] **核对**：每个指针文件里**没有任何实质规则**，只指回 `AGENTS.md`（有规则=漂移，搬回去）
- [ ] 落地前核对各工具当时文档（入口约定随版本变，见 [agents.md](https://agents.md/)）

### 7.2 红线守门（机制 2.5，**不可跳过**——跳过等于没有 harness）

> 每条 HARNESS §8 红线必须有一道对应闸门。详见 [`templates/enforcement/README.md`](templates/enforcement/README.md)。

- [ ] 拷 `enforcement/scripts/check-redlines.sh` 到项目 `scripts/`，改 `INCLUDES` 为目标语言后缀，逐条填 `check(...)` 与 §8 编号对齐
- [ ] 按语言拷守门骨架：TS → `enforcement/ts/eslint.config.skeleton.ts`；Java → `enforcement/java/`（ArchUnit）；Python → `enforcement/python/pyproject-redlines.toml`（import-linter+ruff+mypy）
- [ ] 拷 `enforcement/commitlint.config.cjs`，`type-enum` 与 commit 规范对齐
- [ ] 拷 `enforcement/ci.yml`，**第一步**是 `bash scripts/check-redlines.sh`
- [ ] 装 pre-commit 钩子（simple-git-hooks / husky / lefthook）：pre-commit 跑 redlines+lint，commit-msg 跑 commitlint
- [ ] 仓库设置里把 CI 设为**合并必需检查**（branch protection）——最易漏，漏了前面全白做
- [ ] **自检**：故意写一行违反红线的代码，跑 `bash scripts/check-redlines.sh`，确认它 `exit 1` 并指出位置。拦不下 = 没接好 = 等于没有。
- [ ] 报错信息包含红线编号、命中位置和修复方向，agent 能据此自我修正

### 7.3 其他接线

- [ ] 关键红线尽量上 lint（比 grep 更精确，能区分边界豁免）
- [ ] 关键红线接 lint 规则（如 `no-restricted-imports`）/ CI 守门，能自动查的别靠人查
- [ ] CI 流水线串起 `<CI_CMD>` 五件套

## 八、起最初几篇 ADR

- [ ] 把「为什么选这套技术栈/分层」写成 ADR-0001 起步
- [ ] adr/README.md「启动期必落地清单」列出主线开发前必须 Accepted 的 ADR

## 自检：是否真的生效

> 三个判据，缺一说明契约还是「摆设」：

1. **可索引**：随便给一个任务，agent 能在 workflow §1 找到对应行吗？
2. **可 grep**：每条红线能用一行命令查吗？
3. **可驳回**：违反红线时，是「直接 reject」还是「讨论一下例外」？后者说明它不是红线。

若由 AI 自动接入，还必须额外确认：

4. **负向验证**：AI 是否故意写过违规探针，并确认守门会失败？
5. **探针清理**：违规探针是否已删除，最终 `check-redlines.sh` 是否恢复通过？
6. **可闭环**：重要目标是否有 Guide、Sensor/人工确认、失败处置和 Owner？
7. **行为可信**：关键 Behaviour 是否有独立于当前实现生成过程的验收证据？
8. **可演进**：重复失败是否进入 Steering Log，模板版本与本地差异是否可追溯？
