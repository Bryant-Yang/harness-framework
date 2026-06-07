# enforcement/ —— 让红线长出牙齿

> 这一层是 harness「有效」与「摆设」的分水岭。
>
> 红线写在 `HARNESS.md §8` 里只是**声明**；真正起作用是因为它被编译成**机械闸门**——
> agent 违反就过不了 lint / CI，合不进主分支。**没有这一层，红线就是没人查的装饰。**

## 核心抽象：契约是「每条红线必须有机械守门命令」，工具是实现细节

框架真正要求的**不是「用 eslint」**，而是「每条红线都得有一道能机械执行的闸门」。守门用 eslint / ArchUnit / import-linter / grep 都行——**换实现、不换契约**。

所以本目录分两层：

```
enforcement/
├── scripts/check-redlines.sh   # 【语言无关共享底座】任何「禁止出现 X」红线都靠它，跨语言只改文件后缀
├── commitlint.config.cjs       # 【语言无关】只校验 git message 文本
├── ci.yml                      # 【骨架】串起闸门，换构建命令即可
├── ts/      eslint.config.skeleton.ts   # JS/TS：no-restricted-imports / no-explicit-any
├── java/    ArchUnitRedlinesTest.java   # Java：ArchUnit 分层/禁依赖 + enforcer/checkstyle
└── python/  pyproject-redlines.toml     # Python：import-linter + ruff + mypy
```

> **80% 跨语言免费**（文档层 + grep 层 + commitlint + CI 骨架），**20% 按语言换闸门**（禁 import/分层那类）。
> Java/Python 用户拷对应子目录骨架即可，不必从零接。

## 三类闸门，按红线性质选

| 红线性质 | TS | Java | Python | 共同底座 |
| --- | --- | --- | --- | --- |
| 禁某 import / 单向分层 | eslint `no-restricted-imports` | ArchUnit | import-linter | — |
| 禁类型逃逸 / 危险写法 | eslint `no-explicit-any` | Error Prone / SpotBugs | ruff / mypy | — |
| 禁某依赖进 classpath | （lockfile 审查） | maven-enforcer | （禁 import） | — |
| **通用「禁止出现 X」** | — | — | — | **`check-redlines.sh`（改后缀，零逻辑改动）** |
| commit 格式 | commitlint | commitlint | commitlint / commitizen | — |
| CI 兜底 | GitHub Actions | 同 CI 换 `mvn verify` | 同 CI 换 `ruff`/`pytest` | `ci.yml` |

## 黄金判据：红线 ⇄ 守门命令，一一对应

每条 `HARNESS §8` 红线**必须**在这里有一行对应的守门命令（grep 模式 / lint 规则 / commitlint 项）。

- 能写出守门命令 → 它是红线，登记进来。
- **写不出守门命令** → 它不是红线，降级到北极星原则或普通规范。别让查不了的东西冒充红线。

> 这条判据把「红线」从一句口号变成可执行物。`HARNESS.template.md §8` 的三列表
> （红线 \| 守门命令 \| 谁拦）就是强制你对每条红线填满这一行。

## 接线步骤

1. 把 `scripts/check-redlines.sh` 拷到项目 `scripts/`，按你的红线填 `check(...)` 行（改 `INCLUDES` 为目标语言后缀）。
2. 按语言拷对应子目录：TS → `ts/eslint.config.skeleton.ts`；Java → `java/`；Python → `python/`。
3. 拷 `commitlint.config.cjs`，`type-enum` 与 `git-commit-conventions.md §3` 对齐。
4. 拷 `ci.yml`，第一步就是 `bash scripts/check-redlines.sh`。
5. 装 pre-commit 钩子（`simple-git-hooks` / `husky` / `lefthook` 任选）：
   - `pre-commit` → `check-redlines.sh` + `lint`
   - `commit-msg` → `commitlint`
6. 在仓库设置里把 CI 设为**合并必需检查**（branch protection）——这一步最容易漏，漏了前面全白做。

## 自检

```bash
# 故意写一行违反红线的代码，确认闸门真的会红：
bash scripts/check-redlines.sh   # 应 exit 1 并指出命中位置
```

闸门拦不下故意的违规 = 闸门没接好，等于没有。
