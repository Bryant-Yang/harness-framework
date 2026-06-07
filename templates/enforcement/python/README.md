# enforcement/python —— Python 红线守门骨架

> 把 HARNESS §8 红线编译成 CI 会拦的闸门。与 TS 的 eslint 同位：**换实现、不换契约**。

## 三类闸门

| 红线类型 | 工具 | 跑命令 |
| --- | --- | --- |
| 禁某 import / 单向分层（主力） | **import-linter** | `lint-imports` |
| 禁某模块 banned-api / 危险写法 | **ruff**（flake8-tidy-imports） | `ruff check .` |
| 禁类型逃逸（禁 `Any`） | **mypy** | `mypy <yourapp>` |
| 通用「禁止出现 X」 | `../scripts/check-redlines.sh`（改 `--include='*.py'`） | pre-commit + CI |
| commit 格式 | `../commitlint.config.cjs`（语言无关）或 commitizen | commit-msg 钩子 |

## 用法

1. 把 `pyproject-redlines.toml` 的各段并入项目 `pyproject.toml`。
2. 安装：`pip install import-linter ruff mypy`
3. 填占位符：`<yourapp>` 根包名、`<acme_legacy>` 被禁的旧依赖、各 `R<n>` 红线号。
4. import-linter 的 `layers` 契约：**列表从高层到低层**，高层可 import 低层，低层 import 高层即报错——这就是「单向分层」红线的机械实现。

## 接线到 CI

```bash
lint-imports          # 分层 / 禁依赖红线
ruff check .          # banned-api / 危险写法
mypy <yourapp>        # 类型逃逸
bash scripts/check-redlines.sh   # 通用 grep 底座
```

任一 exit≠0 即 CI 红。把这串放进 `../ci.yml` 的 gates job，换掉 pnpm 那几步即可。

> 共享层（grep 脚本 / commitlint / CI 骨架）见上一级 [`../README.md`](../README.md)，跨语言零改动。
