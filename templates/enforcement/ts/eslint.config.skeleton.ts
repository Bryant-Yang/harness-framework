// 红线守门骨架（JS/TS 项目）—— no-restricted-imports 把「禁止引用」类红线
// 编译成 lint error：违反即过不了 `eslint .`，CI 直接拦。
//
// 关键经验（来自 dw_gis3d 踩坑）：用 regex 而不是 path group。
// gitignore-style glob 会把 `~/foo/bar` 的 basename 误判成 `foo`，
// 导致走二次导出边界的合法内部引用也被误杀。regex 精确锚定包名。
//
// @author <AUTHOR>
import tseslint from 'typescript-eslint'

// 红线：禁止从业务层直接引用某些重依赖 / 被替换的旧依赖。
// 与 HARNESS §8 的 R<n> 对齐，message 里写清红线号，违规时一眼知道踩了哪条。
const RESTRICT_IMPORTS = [
  'error',
  {
    patterns: [
      {
        // 示例：禁止业务层裸引重依赖，必须走 ~/<封装层> 二次导出
        regex: '^<heavydep>(/.+)?$|^@<heavydep>/.+$',
        message: '禁止从业务层引入 <heavydep>；走 ~/<封装层> 二次导出（HARNESS R<n>）',
      },
      {
        // 示例：被替换的旧依赖禁止任何形式复活
        regex: '^<legacy>(/.+)?$|^@<legacy-scope>/.+$',
        message: '禁止任何形式的 <legacy> 引用（项目使命，HARNESS R<n>）',
      },
    ],
  },
] as const

export default tseslint.config(
  { ignores: ['dist/**', 'node_modules/**', 'coverage/**'] },
  {
    rules: {
      // 红线：禁止类型逃逸（HARNESS §8）
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/consistent-type-imports': 'error',
      // 全局禁止表
      'no-restricted-imports': RESTRICT_IMPORTS,
    },
  },
  {
    // 边界豁免：只有封装层 / 适配层可以引那个重依赖。
    // 这一段是「单向依赖」红线的机械实现：业务层禁、封装层放行。
    files: ['src/<封装层>/**', 'src/adapters/**'],
    rules: {
      'no-restricted-imports': 'off',
    },
  },
)
