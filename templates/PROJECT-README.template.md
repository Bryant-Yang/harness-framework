# <PROJECT>

> <一句话项目定位：技术栈 + 它是什么>
>
> 项目使命：<MISSION>

<!-- 这是新工程根目录的 README，做全套文档的总入口。重命名为 README.md。 -->

## 文档地图（按角色）

| 你是谁 / 你要做什么 | 直接读 |
| --- | --- |
| 业务 / 产品同事 | [`docs/SPEC.md`](docs/SPEC.md) + [`docs/glossary.md`](docs/glossary.md) |
| 新加入的开发 | [`docs/workflow.md`](docs/workflow.md) → [`HARNESS.md`](HARNESS.md) §0/§8 → 跑通本地 dev |
| 写新业务功能 | [`docs/SPEC.md`](docs/SPEC.md) + [`docs/data-contracts.md`](docs/data-contracts.md) |
| 改 <核心封装层> | [`HARNESS.md`](HARNESS.md) §4.x |
| 改 UI 组件 | [`HARNESS.md`](HARNESS.md) §4.x UI 段 + [`docs/deps-and-configs.md`](docs/deps-and-configs.md) |
| 加 / 改 / 删依赖 | [`docs/deps-and-configs.md`](docs/deps-and-configs.md) + [`docs/adr/README.md`](docs/adr/README.md) |
| 起 ADR | [`docs/adr/_template.md`](docs/adr/_template.md) |
| 评审 PR | [`HARNESS.md`](HARNESS.md) §8 红线 + [`docs/workflow.md`](docs/workflow.md) §5 提交前自查 |
| 看 Harness 覆盖 / 重复失败 | [`docs/harness-controls.md`](docs/harness-controls.md) |
| 提交代码 / 起 commit | [`docs/git-commit-conventions.md`](docs/git-commit-conventions.md) |
| 看里程碑 / DoD | [`docs/roadmap.md`](docs/roadmap.md) |

## 文档结构

```
<PROJECT>/
├── README.md                # 本文：极简首页 + 文档地图
├── AGENTS.md                # agent 入场契约（唯一契约源，多数工具原生读取）
├── CLAUDE.md                # ┐ 多工具入口指针：内容只指回 AGENTS.md
├── GEMINI.md                # ┘ （按团队用的工具增减）
├── HARNESS.md               # 工程契约：使命、北极星、目录、红线
└── docs/
    ├── SPEC.md              # 业务规格总纲
    ├── workflow.md          # 工作流：典型场景 → 文档 + 红线对照
    ├── harness-controls.md  # Guide / Sensor / SPEC 引用 / Context Routing / Experience Promotion
    ├── git-commit-conventions.md
    ├── adr/                 # 决策记录（README + _template + NNNN-标题.md）
    └── decisions/           # 业务决议卡状态汇总
```

## 快速启动

```bash
<install 命令>
<dev / typecheck / lint / test / build 命令>
```

## 协作纪律

- <语言>沟通，必要术语保留英文。
- `git add` 必须显式列出文件，禁止 `git add .` / `git add -A`。
- 提交前必跑 typecheck + lint + 相关测试。
- 任何对外契约变更（接口 / 数据契约 / 红线 / 依赖）必经 ADR。
- 业务决议卡 ⏳ 状态阻断对应里程碑启动。
- 关键 Behaviour 的独立证据以 SPEC 为唯一事实源；重复失败或高严重度逃逸先形成 Candidate，经评测与 Owner 批准后才晋级。
