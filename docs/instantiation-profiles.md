# 实例化组合

组合是选材指南，不是每次业务任务的流程。旧项目在任一组合上增量合并，已有 Owner Doc 可以保留路径。

| 组合 | 适用 | 必需事实源 | 可选材料 |
| --- | --- | --- | --- |
| minimal | 小工具 / 工程库 | AGENTS、HARNESS、workflow、Controls | README 保留已有内容；按实际 Git 路径补提交规则；有重大决策再加 ADR |
| product | 真实业务产品 | minimal + SPEC（或既有 Behaviour Owner Doc） | 按任务加 roadmap、数据契约、ADR、提交规范、工具指针 |
| legacy overlay | 已有历史债 | 所选组合 + Controls 内批准 baseline 的链接和命令 | 观察模式、收紧计划；不要求历史命中全部清零 |

新 minimal 项目使用 `templates/minimal/` 四份模板。product 使用根模板，删去未使用的行 / 节和链接，或补齐链接的事实源。模板只提供结构，不直接复制全部文件；占位符必须变成项目事实。

```bash
python3 /path/to/harness-framework/scripts/validate-instantiation.py /path/to/project --profile minimal
python3 /path/to/harness-framework/scripts/validate-instantiation.py /path/to/project --profile product --legacy
# 保留旧 Owner Doc 的路径
python3 /path/to/harness-framework/scripts/validate-instantiation.py /path/to/project --profile product \
  --owner direction=docs/architecture.md --owner behaviour=docs/product.md
```

检查从入口与指定事实源沿本地 Markdown 链接读取，验证文件和锚点、框架占位符和未改名模板。保留的 ADR `_template.md` 属于写作工具，可以带占位符；其他已实例化文档不能带占位符。Legacy 在 Controls 用 baseline / 基线链接标签明确绑定已批准文件，不限制文件名。检查只确认链接存在，不证明批准真实性或扫描正确性；实际 baseline Gate 和人类授权仍须验证。

这些检查不验证业务语义，不判断所有重要路径都被路由，也不代替项目 Sensors。任一版本升级必须保留本地事实，并记录来源版本与 commit。
