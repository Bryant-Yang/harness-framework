/**
 * commitlint 配置 —— commit-msg 钩子拦截不符合
 * docs/git-commit-conventions.md 格式的 message。
 *
 * 把「提交规范」从自觉变成机械闸门：type 不在白名单 / subject 空 → 直接驳回。
 *
 * type-enum 必须与 docs/git-commit-conventions.md §3 一一对齐（单一源原则）。
 *
 * @author <AUTHOR>
 */
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      ['feat', 'fix', 'perf', 'refactor', 'style', 'docs', 'test', 'build', 'ci', 'chore', 'revert'],
    ],
    'type-empty': [2, 'never'],
    'subject-empty': [2, 'never'],
    // 中文 commit 不适用 sentence-case，关掉避免误拦
    'subject-case': [0],
    // 禁止句末句号（含中文「。」）
    'subject-full-stop': [2, 'never', '。'],
    // type(scope) 含中文/长 scope 时易超 72，给到 120 兜底；真正 ≤72 由规范自觉
    'header-max-length': [2, 'always', 120],
    'body-max-line-length': [0],
    'footer-max-line-length': [0],
    // scope 白名单：取消注释并填入你的目录/分层，强制 scope 规范化
    // 'scope-enum': [2, 'always', ['<层1>', '<层2>', '<模块>']],
  },
}
