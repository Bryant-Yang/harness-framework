#!/usr/bin/env python3
"""Compare lexical scanner findings as a multiset; never hide scanner errors."""
import argparse
from collections import Counter
from pathlib import Path
import re
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['capture', 'check'])
    parser.add_argument('baseline', type=Path)
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    if not command:
        raise ValueError('scanner command is required after --')
    result = subprocess.run(command, text=True, capture_output=True)
    if result.stderr:
        print(result.stderr, file=sys.stderr, end='')
    if result.returncode not in (0, 1):
        raise ValueError(f'scanner exited {result.returncode}')
    if result.returncode == 1 and (result.stdout or result.stderr):
        raise ValueError('no-match exit status with output / diagnostics; unsupported scanner')
    if result.returncode == 0 and not result.stdout:
        raise ValueError('match exit status without findings; unsupported scanner')
    # Require file:line:content, remove only the line number. Keep duplicate findings.
    findings = []
    for line in result.stdout.splitlines():
        match = re.match(r'^(.+?):[0-9]+:(.*)$', line)
        if not match:
            raise ValueError(f'unsupported scanner output: {line}')
        findings.append(f'{match[1]}:{match[2]}')
    current = Counter(findings)
    if args.mode == 'capture':
        if args.baseline.exists():
            raise ValueError('baseline exists; tighten or replace only with explicit review')
        args.baseline.parent.mkdir(parents=True, exist_ok=True)
        args.baseline.write_text(''.join(f'{x}\n' for x in sorted(findings)))
        print(f'CAPTURED: {len(findings)} findings; approve this baseline before use')
        return 0
    baseline = Counter(args.baseline.read_text().splitlines())
    added = current - baseline
    if added:
        for finding, count in sorted(added.items()):
            print(f'FAIL: +{count} {finding}')
        return 1
    print('PASS: no new findings against approved baseline')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        sys.exit(2)
