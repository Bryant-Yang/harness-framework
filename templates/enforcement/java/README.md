# enforcement/java —— Java 红线守门骨架

> 把 HARNESS §8 红线编译成 `mvn verify` / `gradle check` 会拦的闸门。
> 与 TS 的 eslint 同位：**换实现、不换契约**（红线三列表照填，「守门命令」列从 eslint 换成下面这些）。

## 主力：ArchUnit（禁依赖 / 单向分层）

`ArchUnitRedlinesTest.java` 是骨架。它以 JUnit 测试形式跑，违反 = 测试失败 = `mvn verify` 红。

- 「禁某 import / 依赖」→ `noClasses().should().dependOnClassesThat()...`
- 「单向分层」→ `layeredArchitecture()...`

填法：改 `@AnalyzeClasses` 的根包、各 `definedBy` 的分层包名、`.as("R<n> ...")` 的红线号。

## 补充闸门（按需叠加）

**Maven enforcer —— 禁止某 Maven 依赖进 classpath**（比代码层 import 更早拦）：

```xml
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-enforcer-plugin</artifactId>
  <executions>
    <execution>
      <id>redline-banned-deps</id>
      <goals><goal>enforce</goal></goals>
      <configuration>
        <rules>
          <bannedDependencies>
            <excludes>
              <exclude><com.acme:legacy></exclude>  <!-- R<n> 旧依赖禁复活 -->
            </excludes>
          </bannedDependencies>
        </rules>
      </configuration>
    </execution>
  </executions>
</plugin>
```

**Checkstyle IllegalImport —— 禁某包的 import**（轻量、无需写测试）：

```xml
<module name="IllegalImport">
  <property name="illegalPkgs" value="<com.acme.legacy>"/>
</module>
```

**Error Prone / SpotBugs** —— 「禁止危险写法」类红线（等价 TS no-explicit-any）。

## 接线

| 红线类型 | 用什么 | 跑在哪 |
| --- | --- | --- |
| 禁 import / 单向分层 | ArchUnit（本目录） | `mvn verify` / `gradle check` → CI |
| 禁某 Maven 依赖 | maven-enforcer bannedDependencies | `mvn verify` |
| 禁某包 import（轻量） | Checkstyle IllegalImport | `mvn verify` |
| 通用「禁止出现 X」 | `../scripts/check-redlines.sh`（改 `--include='*.java'`） | pre-commit + CI |
| commit 格式 | `../commitlint.config.cjs`（语言无关） | commit-msg 钩子 |

> 共享层（grep 脚本 / commitlint / CI 骨架）见上一级 [`../README.md`](../README.md)，跨语言零改动。
