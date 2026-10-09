#!/usr/bin/env python3
"""Adversarial probes for shipped lexical scanners and baseline comparison."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import sys

ROOT = Path(__file__).resolve().parents[1]
COUNT = 0


def run(command, cwd, status, diagnostic=None, env=None):
    global COUNT
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, env=env)
    assert result.returncode == status, (command, result.returncode, result.stdout, result.stderr)
    if diagnostic:
        assert diagnostic in result.stdout + result.stderr, (diagnostic, result.stdout, result.stderr)
    COUNT += 1
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--with-toolchains', action='store_true')
    args = parser.parse_args()
    sample = ROOT / 'examples/node-orders-api'
    with tempfile.TemporaryDirectory(prefix='harness-enforcement-') as name:
        project = Path(name) / 'project'
        shutil.copytree(sample, project)
        script = project / 'scripts/check-redlines.sh'
        original = script.read_text()
        command = ['bash', str(script)]
        run(command, project, 0, 'PASS')
        cases = [
            ('R1', 'domain', "import { PrismaClient } from '@prisma/client'"),
            ('R2', 'services', "import x from '@acme/monolith'"),
            ('R3', 'domain', 'const x = {} as any'),
            ('R4', 'services', 'const x = process.env.TOKEN'),
            ('R5', 'services', "console.log('x')"),
            ('R6', 'routes', "const sql = 'SELECT id FROM orders'"),
        ]
        for rule, folder, code in cases:
            probe = project / f'src/{folder}/probe.ts'
            probe.write_text(code)
            run(command, project, 1, f'FAIL [{rule}]')
            probe.unlink()
        run(command, project, 0)
        script.write_text(original.replace('check "R2"', '# check "R2"'))
        run(command, project, 2, 'ERROR [R2]')
        script.write_text('\n'.join('check \"R1\" \"bad regex\" \"[\" src/domain' if line.startswith('check \"R1\"') else line for line in original.splitlines()) + '\n')
        run(command, project, 2, 'ERROR [R1]')
        script.write_text(original)
        shutil.rmtree(project / 'src/domain')
        run(command, project, 2, 'missing search path')
        (project / 'src/domain').mkdir()
        fake_bin = Path(name) / 'bin'
        fake_bin.mkdir()
        (fake_bin / 'grep').write_text('#!/bin/sh\necho scanner-error >&2\nexit 2\n')
        (fake_bin / 'grep').chmod(0o755)
        run(command, project, 2, 'scanner-error', env={**os.environ, 'PATH': str(fake_bin) + os.pathsep + os.environ['PATH']})
        template = (ROOT / 'templates/enforcement/scripts/check-redlines.sh').read_text()
        script.write_text(template)
        run(command, project, 2, 'no rules configured')
        # The lexical skeleton works across configured extensions, without claiming AST coverage.
        for ext in ('ts', 'py', 'java'):
            configured = template.replace('EXPECTED_IDS=()', 'EXPECTED_IDS=(R1)')
            configured = configured.replace("--include='*.ts'", f"--include='*.{ext}'")
            script.write_text(configured.replace('\nfinish\n', '\ncheck "R1" "forbidden literal" "legacy_marker" src\nfinish\n'))
            probe = project / f'src/domain/probe.{ext}'
            probe.write_text('safe_marker\n')
            run(command, project, 0)
            probe.write_text('legacy_marker\n')
            run(command, project, 1, 'FAIL [R1]')
            probe.unlink()
        baseline = Path(name) / 'baseline.txt'
        source = Path(name) / 'source.ts'
        source.write_text('legacy_marker\n')
        scanner = ['grep', '-nH', 'legacy_marker', str(source)]
        base_cmd = [sys.executable, str(ROOT / 'scripts/check-baseline.py')]
        run(base_cmd + ['capture', str(baseline), '--'] + scanner, project, 0)
        run(base_cmd + ['check', str(baseline), '--'] + scanner, project, 0)
        source.write_text('\n\nlegacy_marker\n')
        run(base_cmd + ['check', str(baseline), '--'] + scanner, project, 0)
        source.write_text('legacy_marker\nlegacy_marker\n')
        run(base_cmd + ['check', str(baseline), '--'] + scanner, project, 1, '+1')
        run(base_cmd + ['capture', str(baseline), '--'] + scanner, project, 2, 'baseline exists')
        run(base_cmd + ['check', str(baseline), '--', 'grep', '-nH', '[', str(source)], project, 2)
        run(base_cmd + ['check', str(baseline), '--', 'grep', '-nH', 'legacy_marker', str(source) + '.missing'], project, 2)
        source.write_text('safe\n')
        run(base_cmd + ['check', str(baseline), '--'] + scanner, project, 0)
        run(base_cmd + ['check', str(baseline), '--', sys.executable, '-c', 'pass'], project, 2, 'without findings')
        run(base_cmd + ['check', str(baseline), '--', sys.executable, '-c', 'import sys; print(\"error\", file=sys.stderr); sys.exit(1)'], project, 2, 'diagnostics')
    print(f'PASS: {COUNT} lexical / error / baseline probes')
    if args.with_toolchains:
        subprocess.run(['npm', 'test', '--prefix', str(ROOT / 'tests/enforcement/ts')], check=True)
    else:
        print('NOT RUN: TypeScript / commitlint; use --with-toolchains after npm ci')


if __name__ == '__main__':
    main()
