/** Project commit conventions: keep type / scope lists aligned with Owner Doc. */
module.exports = {
  extends: ['@commitlint/config-conventional'],
  plugins: [{
    rules: {
      'subject-ending': ({ subject }) => [
        !subject || !/\p{P}$/u.test(subject),
        'subject must not end with punctuation',
      ],
    },
  }],
  rules: {
    'type-enum': [2, 'always', ['feat', 'fix', 'perf', 'refactor', 'style', 'docs', 'test', 'build', 'ci', 'chore', 'revert']],
    'type-empty': [2, 'never'],
    'subject-empty': [2, 'never'],
    // Chinese has no letter case; enforce the chosen English convention in review.
    'subject-case': [0],
    'subject-max-length': [2, 'always', 72],
    'subject-ending': [2, 'always'],
    'header-max-length': [2, 'always', 120],
    'body-max-line-length': [2, 'always', 100],
    'footer-max-line-length': [0],
    // 'scope-enum': [2, 'always', ['<module-one>', '<module-two>']],
  },
}
