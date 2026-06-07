// 红线守门骨架（Java）—— ArchUnit 把「禁某依赖 / 单向分层」类红线编译成 JUnit 测试：
// 违反即 `mvn verify` / `gradle check` 失败，CI 直接拦。等价于 TS 的 eslint no-restricted-imports。
//
// 依赖（test scope）：
//   Maven:  com.tngtech.archunit:archunit-junit5:1.3.0
//   Gradle: testImplementation 'com.tngtech.archunit:archunit-junit5:1.3.0'
//
// 每条 @ArchTest 的 .as(...) 里写清红线号，违规报错时一眼知道踩了 HARNESS §8 哪条。
//
// @author <AUTHOR>
package redlines;

import com.tngtech.archunit.core.importer.ImportOption;
import com.tngtech.archunit.junit.AnalyzeClasses;
import com.tngtech.archunit.junit.ArchTest;
import com.tngtech.archunit.lang.ArchRule;

import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.noClasses;
import static com.tngtech.archunit.library.Architectures.layeredArchitecture;

@AnalyzeClasses(packages = "<com.acme.yourapp>", importOptions = ImportOption.DoNotIncludeTests.class)
class ArchUnitRedlinesTest {

    // R<n> 单向分层依赖：上层可依赖下层，下层不可反向（等价 TS eslint files 段豁免）
    @ArchTest
    static final ArchRule LAYERED = layeredArchitecture().consideringAllDependencies()
            .layer("Web").definedBy("..web..", "..controller..")
            .layer("Service").definedBy("..service..")
            .layer("Domain").definedBy("..domain..")
            .layer("Db").definedBy("..repository..", "..db..")
            .whereLayer("Web").mayNotBeAccessedByAnyLayer()
            .whereLayer("Service").mayOnlyBeAccessedByLayers("Web")
            .whereLayer("Domain").mayOnlyBeAccessedByLayers("Web", "Service", "Db")
            .whereLayer("Db").mayOnlyBeAccessedByLayers("Service")
            .as("R<n> 单向分层：domain 不依赖 web/db");

    // R<n> domain 是纯业务，禁止依赖持久化框架（等价 TS 的 domain 禁 import prisma）
    @ArchTest
    static final ArchRule DOMAIN_PURE = noClasses()
            .that().resideInAPackage("..domain..")
            .should().dependOnClassesThat().resideInAnyPackage("jakarta.persistence..", "org.hibernate..", "..repository..")
            .as("R<n> domain/ 必须纯业务，禁止依赖持久化框架");

    // R<n> 被替换的旧依赖禁止复活（等价 TS 的禁 @acme/monolith）
    @ArchTest
    static final ArchRule NO_LEGACY = noClasses()
            .should().dependOnClassesThat().resideInAPackage("<com.acme.legacy>..")
            .as("R<n> 被拆分的旧单体禁止复活");
}
