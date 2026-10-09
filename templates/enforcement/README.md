# 让启用控制真正守门

每条启用的机械红线都要有实际检查；观察模式、待实现规则、语义 review 和人工验收分别登记，不能宣称全部已执行。

## 接线

1. 从 HARNESS §8 选启用的阻断规则，确定输入范围、匹配语义与检测边界。
2. 复制 `scripts/check-redlines.sh` 到项目 `scripts/`，独立填写 `EXPECTED_IDS` 和启用的 `check` 行，改语言后缀与路径。未配置模板返回 ERROR，不能当绿灯。
3. 对语法 / 结构保证接 AST / lint / 结构测试。TS 骨架注册 parser / plugin，适配层仅豁免重依赖，不豁免全局旧依赖禁令。
4. 有对应提交规范时复制 commitlint 配置，并将 CLI 和 preset 写进项目 lockfile；CI 骨架检查 PR / push 范围。本地 commit-msg hook 只能补充，不能替代 CI。
5. 合并到现有 CI，按实际授权配置 required checks / branch protection；无权限则列出具体外部待办。
6. 验证每条规则的合法、违规与错误输入；清理本次探针，必要检查再通过。失败反馈要能定位规则、文件和修复事实源。

## 结果与检测边界

`check-redlines.sh`：0 = PASS，1 = 违规 FAIL，2 = 配置 / 扫描 ERROR。CI 两种非零都阻断。规则缺失、重复、搜索路径缺失、正则或工具出错不能显示通过。`EXPECTED_IDS` 由已批准契约维护，不能随着删除 `check` 行同步削弱。

grep 只检查有限文本模式，可能漏掉多行、动态 import、别名、计算属性，也可能命中注释 / 字符串。不得据此保证“任何形式引用”或业务语义。TypeScript `no-restricted-imports` 骨架覆盖静态 import / export；动态 import / require / 间接访问需按实际项目补 AST 控制和探针。Java / Python 目录提供可接入骨架，本框架本轮未执行 ArchUnit、ruff、mypy、import-linter 的实际 toolchain；跨语言 grep smoke 不能冒充这些验证。

## Legacy baseline

框架 `scripts/check-baseline.py` 采集 `文件:行号:内容` 输出，移除行号但保留文件、内容及重复次数；历史移动不误报，同文件新增同样命中仍失败。扫描命令只允许 0 = 有命中、1 = 无命中；其他返回码报 ERROR。不要以 `|| true` 吞错。

```bash
python3 /path/to/framework/scripts/check-baseline.py capture docs/baselines/R1.txt -- \
  rg -n --no-heading --color never 'legacy-lib' src
# baseline 经对应 Owner 批准并纳入版本控制后，CI 使用同一命令
python3 /path/to/framework/scripts/check-baseline.py check docs/baselines/R1.txt -- \
  rg -n --no-heading --color never 'legacy-lib' src
```

已有 baseline 不会被 capture 覆盖。更换匹配模式、扫描目录或批准扩大时明确 review；文本 baseline 允许等量等内容的移动，不保证每个语义引用的身份。

## 框架自身验证

```bash
python3 scripts/test-enforcement.py
npm ci --prefix tests/enforcement/ts --ignore-scripts
python3 scripts/test-enforcement.py --with-toolchains
```

验证直接运行发货的脚本和 TS 骨架，包含各文本规则、漏配、坏正则、缺路径、scanner failure、baseline、新增重复命中、TS 正反例与 commitlint。普通 Python probes 不执行 TS，输出明确 NOT RUN；仓库 CI 必须执行锁定 toolchain fixture。
