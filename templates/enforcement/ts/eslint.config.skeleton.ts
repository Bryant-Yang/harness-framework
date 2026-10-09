// Replace package / wrapper placeholders and run positive and negative probes.
// no-restricted-imports covers static import/export only. For dynamic imports,
// require() and indirect access use an AST rule matched to the project's runtime.
import tseslint from 'typescript-eslint'

const legacyPatterns = [
  {
    regex: '^<legacy>(/.+)?$|^@<legacy-scope>/.+$',
    message: 'R-legacy: use the approved replacement',
  },
]
const heavyPatterns = [
  {
    regex: '^<heavydep>(/.+)?$|^@<heavydep>/.+$',
    message: 'R-boundary: import from the approved wrapper',
  },
]

export default tseslint.config(
  { ignores: ['dist/**', 'node_modules/**', 'coverage/**'] },
  ...tseslint.configs.recommended,
  {
    files: ['**/*.ts', '**/*.tsx'],
    rules: {
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/consistent-type-imports': 'error',
      'no-restricted-imports': ['error', { patterns: [...legacyPatterns, ...heavyPatterns] }],
    },
  },
  {
    files: ['src/<封装层>/**', 'src/adapters/**'],
    rules: {
      // The wrapper exemption never removes the global legacy prohibition.
      'no-restricted-imports': ['error', { patterns: legacyPatterns }],
    },
  },
)
