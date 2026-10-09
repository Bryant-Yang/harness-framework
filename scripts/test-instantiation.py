#!/usr/bin/env python3
"""Render the shipped minimal templates and probe document closure."""
import importlib.util
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('validator', ROOT / 'scripts/validate-instantiation.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


def main():
    count = 0
    with tempfile.TemporaryDirectory(prefix='harness-instance-') as name:
        root = Path(name)
        facts = {'PROJECT': 'small-tool', 'BASELINE': 'existing CLI', 'MISSION': 'validate public CLI without changing external systems',
                 'EVIDENCE': 'CLI positive / invalid input probes', 'OWNER': 'maintainer', 'CONTROLS': 'C1: python3 check.py; errors block',
                 'SCENE': 'CLI changes / scripts', 'OUTPUT': 'implementation and probes', 'SOURCE_SHA': 'edf5261',
                 'LOCAL_DELTA': 'none', 'LEGACY_STATUS': 'no historical debt'}
        for source in (ROOT / 'templates/minimal').rglob('*.template.md'):
            dest = root / str(source.relative_to(ROOT / 'templates/minimal')).replace('.template', '')
            dest.parent.mkdir(parents=True, exist_ok=True)
            text = source.read_text()
            for key, value in facts.items():
                text = text.replace(f'<{key}>', value)
            dest.write_text(text)
        def check(profile='minimal', legacy=False, expect=None, owners=None):
            nonlocal count
            errors, _ = validator.validate(root, profile, legacy, owners or validator.DEFAULT_OWNERS)
            assert (not errors) if expect is None else any(expect in x for x in errors), errors
            count += 1
        check()
        (root / 'HARNESS.md').write_text((root / 'HARNESS.md').read_text() + '\n```ts\nfunction identity<T>(x: T): T { return x }\n```\n')
        check()
        check('product', expect='missing document')
        (root / 'docs/SPEC.md').write_text('# Public behaviour\n\n## Evidence\n\nExisting user acceptance examples.\n')
        controls = root / 'docs/harness-controls.md'
        original = controls.read_text()
        controls.write_text(original + '\n[Behaviour](SPEC.md#evidence)\n')
        check('product')
        controls.write_text(original + '\n[Behaviour](SPEC.md#missing)\n')
        check('product', expect='missing anchor')
        controls.write_text(original + '\n[Missing](missing.md)\n')
        check(expect='broken link')
        controls.write_text(original + '\n<PROJECT>\n')
        check(expect='unresolved')
        controls.write_text(original + '\n[Candidate](draft.template.md)\n')
        (root / 'docs/draft.template.md').write_text('# Draft\n')
        check(expect='unrenamed')
        controls.write_text(original)
        check(legacy=True, expect='legacy:')
        (root / 'docs/baselines').mkdir()
        (root / 'docs/baselines/R1.txt').write_text('src/old.ts:legacy\n')
        controls.write_text(original + '\n[Approved baseline](baselines/R1.txt); capture and check via project scanner.\n')
        check(legacy=True)
        (root / 'docs/debt.json').write_text('{}')
        controls.write_text(original + '\n[Approved baseline](debt.json)\n')
        check(legacy=True)
        controls.write_text(original + '\n[历史基线](debt.json)\n')
        check(legacy=True)
        controls.write_text(original + '\n[Escape](../../outside.md)\n')
        check(expect='outside project')
        controls.write_text(original)
        (root / 'HARNESS.md').rename(root / 'architecture.md')
        for p in (root / 'AGENTS.md', root / 'docs/workflow.md', controls):
            p.write_text(p.read_text().replace('HARNESS.md', 'architecture.md'))
        check(owners={**validator.DEFAULT_OWNERS, 'direction': 'architecture.md'})
    print(f'PASS: {count} minimal / product / legacy / owner / broken-reference probes')


if __name__ == '__main__':
    main()
