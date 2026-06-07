# Git 提交规则（<PROJECT>）

> 作者：<AUTHOR>　最近更新：<YYYY-MM-DD>
>
> 本文是 <PROJECT> 唯一的提交规范来源。所有 PR、所有 commit 必走本文。
>
> 上游约束：[`../HARNESS.md`](../HARNESS.md) §3 工程规范、§8 红线。

## 1. 一句话规则

**`type(scope): subject` + 必要时 body 解释 why + 必要时 footer 标 BREAKING / Closes**——任何不符合本格式的提交，CI `commitlint` 直接驳回。

## 2. 完整格式

```
<type>(<scope>): <subject>
<空行>
<body：可选，解释为什么这么改，不解释代码本身在做什么>
<空行>
<footer：可选，BREAKING CHANGE / Closes #N / Refs #N / Co-Authored-By>
```

约束：

- **subject ≤ 72 字符**，命令式（"add" 不是 "added"），首字小写，结尾**无标点**。
- **body 每行 ≤ 100 字符**，一段一空行。统一**正文<语言> + type 英文**。
- **type 必须小写**，列表见 §3。
- **scope 选填但强烈建议填**，列表见 §4。
- **整个 commit message 必须以 LF 结尾**（不要 CRLF）。

## 3. type（标准 11 种）

| type | 用途 | 触发版本 |
| --- | --- | --- |
| `feat` | 新功能（业务或对外可见的能力） | minor |
| `fix` | bug 修复 | patch |
| `perf` | 性能优化（无功能变化） | patch |
| `refactor` | 重构（无功能变化、无性能变化） | — |
| `style` | 代码格式（空格、分号、缩进、命名） | — |
| `docs` | 文档 | — |
| `test` | 增 / 改 / 删测试 | — |
| `build` | 构建系统、打包配置 | — |
| `ci` | CI / CD 配置 | — |
| `chore` | 杂务（依赖升级、目录重组） | — |
| `revert` | 回滚某个提交（搭配 `Reverts: <sha>` footer） | — |

**辨析容易混的几对：**

- `feat` vs `refactor`：是否带来新的对外行为？是 → feat，不是 → refactor。
- `fix` vs `revert`：bug 是新引入还是历史已有？新引入用 revert，历史已有用 fix。
- `chore` vs `build`：与构建产物的生成路径有关用 build，纯依赖/工具链升级用 chore。
- `style` vs `refactor`：style 不改 AST（仅格式），refactor 改 AST 但不改对外行为。

## 4. scope（按本项目目录约定）

| scope | 含义 |
| --- | --- |
| `<层/模块名>` | `src/<...>/**` |
| … | … |

> 按你的目录结构填。scope 应与 HARNESS 目录树/分层一致。

## 5. 硬约束（与 AGENTS / HARNESS 对齐）

- `git add` 必须显式列文件，禁止 `git add .` / `git add -A`。
- 禁止 `--no-verify` / `--no-gpg-sign`。
- 主分支禁止 force push；feature 分支仅 `--force-with-lease`。
- 引入 `BREAKING CHANGE` 必须配 ADR。

## 6. commitlint 配置

把 type/scope 白名单同步进 `commitlint.config.cjs`，让 §3/§4 由 CI 强制，而不是靠自觉。
