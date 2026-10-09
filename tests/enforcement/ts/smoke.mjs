// Exercise the shipped skeleton, not a second independently maintained config.
import { ESLint } from 'eslint'
import ts from 'typescript'
import { readFile, writeFile, mkdtemp, rm, mkdir, chmod } from 'node:fs/promises'
import path from 'node:path'
import { fileURLToPath, pathToFileURL } from 'node:url'
import { spawnSync } from 'node:child_process'
import assert from 'node:assert/strict'

const fixture = path.dirname(fileURLToPath(import.meta.url))
const root = path.resolve(fixture, '../../..')
const temp = await mkdtemp(path.join(fixture, '.smoke-'))
let count = 0
try {
  const source = (await readFile(path.join(root, 'templates/enforcement/ts/eslint.config.skeleton.ts'), 'utf8'))
    .replaceAll('<legacy>', 'legacy-lib').replaceAll('<legacy-scope>', 'old')
    .replaceAll('<heavydep>', 'heavydep').replaceAll('<封装层>', 'wrappers')
  const compiled = ts.transpileModule(source, { compilerOptions: { module: ts.ModuleKind.ESNext } }).outputText
  const configPath = path.join(temp, 'config.mjs')
  await writeFile(configPath, compiled)
  const { default: config } = await import(pathToFileURL(configPath).href)
  const eslint = new ESLint({ cwd: temp, overrideConfigFile: true, overrideConfig: config })
  const cases = [
    ['src/domain/a.ts', "import x from 'heavydep'; void x", 'no-restricted-imports'],
    ['src/domain/a.ts', "import {\n value\n} from 'heavydep'; void value", 'no-restricted-imports'],
    ['src/domain/a.ts', "export { value } from 'legacy-lib'", 'no-restricted-imports'],
    ['src/adapters/a.ts', "import x from 'heavydep'; void x", null],
    ['src/wrappers/a.ts', "import x from 'heavydep'; void x", null],
    ['src/adapters/a.ts', "import x from 'legacy-lib'; void x", 'no-restricted-imports'],
    ['src/wrappers/a.ts', "import x from '@old/lib'; void x", 'no-restricted-imports'],
    ['src/domain/a.ts', "const x = {} as\n any; void x", '@typescript-eslint/no-explicit-any'],
    ['src/domain/a.ts', "import x from '~/heavydep/wrapper'; void x", null],
    ['src/domain/a.ts', 'const x: number = 1; void x', null],
  ]
  for (const [filePath, code, expected] of cases) {
    const [result] = await eslint.lintText(code, { filePath: path.join(temp, filePath) })
    assert.equal(result.fatalErrorCount, 0, JSON.stringify(result.messages))
    if (expected) assert(result.messages.some(x => x.ruleId === expected), `${filePath}: expected ${expected}`)
    else assert.equal(result.errorCount, 0, JSON.stringify(result.messages))
    count++
  }
  const [invalid] = await eslint.lintText('const =', { filePath: path.join(temp, 'src/domain/a.ts') })
  assert(invalid.fatalErrorCount > 0, 'syntax errors must not become green')
  count++
  // This limitation is deliberate and documented: static import rule misses import().
  const [dynamic] = await eslint.lintText("void import('legacy-lib')", { filePath: path.join(temp, 'src/domain/a.ts') })
  assert(!dynamic.messages.some(x => x.ruleId === 'no-restricted-imports'))
  count++
  for (const [message, status] of [['feat(harness): evolve experience controls\n', 0], ['invalid message\n', 1], ['fix: ' + 'x'.repeat(73) + '\n', 1], ['fix: ends with a period.\n', 1], ['fix: 修复门禁。\n', 1]]) {
    const result = spawnSync(path.join(fixture, 'node_modules/.bin/commitlint'),
      ['--config', path.join(root, 'templates/enforcement/commitlint.config.cjs')],
      { cwd: fixture, input: message, encoding: 'utf8', env: { ...process.env, NODE_PATH: path.join(fixture, 'node_modules') } })
    assert.equal(result.status, status, result.stderr + result.stdout)
    count++
  }
  // Run the actual CI first-push block against a two-commit repository.
  const ci = await readFile(path.join(root, 'templates/enforcement/ci.yml'), 'utf8')
  const pushStep = ci.split('      - name: Commit messages (push range)')[1].split('\n      - name: Typecheck')[0]
  assert(pushStep.includes('        shell: bash'), 'CI must enable bash pipefail for first-push scanning')
  const pushBlock = pushStep
    .split('        run: |\n')[1].split('\n      - name: Typecheck')[0].replace(/^ {10}/gm, '')
  const repo = path.join(temp, 'commit-range')
  await mkdir(repo)
  const git = (...args) => {
    const result = spawnSync('git', args, { cwd: repo, encoding: 'utf8' })
    assert.equal(result.status, 0, result.stderr)
    return result.stdout.trim()
  }
  git('init', '--quiet')
  git('config', 'user.name', 'Harness Fixture')
  git('config', 'user.email', 'fixture@example.invalid')
  git('commit', '--quiet', '--allow-empty', '-m', 'invalid earlier message')
  git('commit', '--quiet', '--allow-empty', '-m', 'feat: valid latest message')
  await writeFile(path.join(repo, 'commitlint.config.cjs'), await readFile(path.join(root, 'templates/enforcement/commitlint.config.cjs')))
  const bin = path.join(temp, 'bin')
  await mkdir(bin)
  // Minimal pnpm shim forwards to the locked fixture binary; it does not alter the CI block.
  await writeFile(path.join(bin, 'pnpm'), '#!/bin/sh\n[ "$1" = exec ] || exit 2\nshift\n[ "$1" = commitlint ] || exit 2\nshift\nexec "$FIXTURE_COMMITLINT" "$@"\n')
  await chmod(path.join(bin, 'pnpm'), 0o755)
  const checkRange = (status, before = '0'.repeat(40), extraEnv = {}) => {
    const result = spawnSync('bash', ['-e', '-o', 'pipefail', '-c', pushBlock], { cwd: repo, encoding: 'utf8',
      env: { ...process.env, PATH: bin + path.delimiter + process.env.PATH,
        FIXTURE_COMMITLINT: path.join(fixture, 'node_modules/.bin/commitlint'), NODE_PATH: path.join(fixture, 'node_modules'),
        BEFORE_SHA: before, HEAD_SHA: git('rev-parse', 'HEAD'), ...extraEnv } })
    assert.equal(result.status, status, result.stderr + result.stdout)
    count++
  }
  checkRange(1)
  const before = git('rev-parse', 'HEAD^')
  checkRange(0, before)
  git('commit', '--quiet', '--allow-empty', '-m', 'invalid newly pushed message')
  checkRange(1, before)
  // Rebuild root as valid then keep a valid head, and test the same initial-push path.
  git('checkout', '--orphan', 'valid-history')
  git('commit', '--quiet', '--allow-empty', '-m', 'feat: valid initial commit')
  git('commit', '--quiet', '--allow-empty', '-m', 'fix: valid second commit')
  checkRange(0)
  const brokenGit = path.join(temp, 'broken-git')
  await mkdir(brokenGit)
  await writeFile(path.join(brokenGit, 'git'), '#!/bin/sh\necho injected-git-error >&2\nexit 128\n')
  await chmod(path.join(brokenGit, 'git'), 0o755)
  checkRange(128, '0'.repeat(40), { PATH: brokenGit + path.delimiter + bin + path.delimiter + process.env.PATH })
  console.log(`PASS: ${count} TypeScript / commitlint checks (dynamic import coverage explicitly excluded)`)
} finally {
  await rm(temp, { recursive: true, force: true })
}
