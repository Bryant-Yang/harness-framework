#!/usr/bin/env python3
"""Framework integrity and executable probes; structural checks do not prove semantics."""
import argparse
import importlib.util
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--with-toolchains', action='store_true')
    args = parser.parse_args()
    version = (ROOT / 'VERSION').read_text().strip()
    require(version == '2.3.0', f'unexpected version: {version}')
    for name in ('README.md', 'docs/HARNESS-ENGINEERING.md', 'templates/HARNESS.template.md', 'templates/docs/harness-controls.template.md'):
        require(version in (ROOT / name).read_text(), f'version drift: {name}')
    for name in ('CLAUDE.md', 'GEMINI.md', '.github/copilot-instructions.md', '.cursor/rules/000-agents.mdc'):
        text = (ROOT / 'templates' / name).read_text()
        require('AGENTS.md' in text and len(text.splitlines()) <= 20 and '\n## ' not in text, f'not a thin pointer: {name}')
    skill = (ROOT / 'SKILL.md').read_text()
    require(skill.startswith('---\nname: harness-framework\n') and len(skill.splitlines()) < 500, 'invalid Skill entry')
    for link in ('AI-ADOPTION-PROTOCOL.md', 'docs/HARNESS-ENGINEERING.md', 'docs/experience-learning.md'):
        require(link in skill, f'Skill missing resource: {link}')
    for name, marker in (
        ('AI-ADOPTION-PROTOCOL.md', 'harness:maintenance-routing=delta-impact'),
        ('AI-ADOPTION-PROTOCOL.md', 'harness:ai-assets-audit=conditional'),
        ('docs/HARNESS-ENGINEERING.md', 'harness:boundary-sensor=producer-contract-consumer'),
        ('templates/AGENTS.template.md', 'harness:controls-read-policy=on-demand'),
        ('templates/docs/SPEC.template.md', 'harness:behaviour-evidence=canonical-source'),
        ('templates/docs/harness-controls.template.md', 'harness:behaviour-evidence=spec-reference-only'),
    ):
        require(marker in (ROOT / name).read_text(), f'missing routing / owner contract: {name}: {marker}')
    ci = (ROOT / '.github/workflows/check-framework.yml').read_text()
    require('bash scripts/check-framework.sh --with-toolchains' in ci and 'npm ci' in ci, 'CI must execute locked toolchains')
    spec = importlib.util.spec_from_file_location('validator', ROOT / 'scripts/validate-instantiation.py')
    validator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(validator)
    # Source templates link to future renamed files; instantiated template probes cover those.
    documents = list(ROOT.glob('*.md')) + list((ROOT / 'docs').glob('*.md')) + list((ROOT / 'examples').rglob('*.md'))
    for doc in documents:
        text = re.sub(r'^```.*?^```\s*$', '', doc.read_text(), flags=re.M | re.S)
        for raw in validator.LINK.findall(text):
            parsed = urlsplit(raw.strip().split(' "', 1)[0].strip('<>'))
            if parsed.scheme or parsed.netloc or '<' in raw or '>' in raw:
                continue
            target = (doc.parent / unquote(parsed.path)).resolve() if parsed.path else doc
            require(target.exists(), f'broken source link: {doc.relative_to(ROOT)}: {raw}')
            if parsed.fragment and target.is_file() and target.suffix == '.md':
                require(unquote(parsed.fragment) in validator.anchors(target.read_text()), f'broken source anchor: {doc.relative_to(ROOT)}: {raw}')
    commands = [
        [sys.executable, 'scripts/test-instantiation.py'],
        [sys.executable, 'scripts/test-enforcement.py'] + (['--with-toolchains'] if args.with_toolchains else []),
        [sys.executable, 'examples/experience-loop/replay.py'],
        [sys.executable, 'scripts/test-skill-install.py'],
    ]
    for command in commands:
        subprocess.run(command, cwd=ROOT, check=True)
    print(f'PASS: Harness Framework {version} integrity and executable probes; model Skill A/B not run')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        sys.exit(1)
