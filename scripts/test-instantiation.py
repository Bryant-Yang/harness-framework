#!/usr/bin/env python3
"""Render shipped minimal and product templates; probe structural closure only."""
import importlib.util
from pathlib import Path
import re
import shutil
import tempfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('validator', ROOT / 'scripts/validate-instantiation.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


def render_product(root):
    # A structural fixture, not a business spec or a claim of model usefulness.
    # Preserve HTML contract markers; replacing them would hide scanner bugs.
    facts = {'PROJECT': 'orders-api', 'AUTHOR': 'Fixture maintainer',
             'YYYY-MM-DD': '2026-10-15', 'MISSION': 'create orders',
             '模块': 'orders', '用例标题': 'create-order',
             '关键用例锚点': 'uc-orders-001-create-order', '锚点': 'uc-orders-001-create-order',
             'SOURCE_PATH': 'src/orders.py', 'ENTRY_SYMBOL': 'create_order',
             'N': '400', 'M': '800', 'sha': '1e9da61'}
    rendered = []
    for source in sorted((ROOT / 'templates').rglob('*.template.md')):
        if 'minimal' in source.relative_to(ROOT / 'templates').parts:
            continue
        relative = str(source.relative_to(ROOT / 'templates')).replace('.template', '')
        if relative == 'PROJECT-README.md':
            relative = 'README.md'
        elif relative == 'docs/subsystem.md':
            relative = 'docs/orders.md'
        dest = root / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        text = re.sub(r'<(?![!/])([^<>\n]+)>', lambda m: facts.get(m[1], 'fixture'), source.read_text())
        dest.write_text(text)
        rendered.append(dest)
    for name in ('CLAUDE.md', 'GEMINI.md', '.github/copilot-instructions.md', '.cursor/rules/000-agents.mdc'):
        dest = root / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / 'templates' / name, dest)
    (root / 'src').mkdir()
    (root / 'src/orders.py').write_text('def create_order(payload):\n    return {"id": payload["id"]}\n')
    # Template for future ADRs intentionally remains unfilled.
    shutil.copy2(ROOT / 'templates/docs/adr/_template.md', root / 'docs/adr/_template.md')
    return rendered


def product_probes():
    count = 0
    with tempfile.TemporaryDirectory(prefix='harness-product-') as name:
        root = Path(name)
        rendered = render_product(root)

        def check(expect=None):
            nonlocal count
            errors, _ = validator.validate(root, 'product', False, validator.DEFAULT_OWNERS)
            assert (not errors) if expect is None else any(expect in x for x in errors), errors
            count += 1

        check()
        controls = root / 'docs/harness-controls.md'
        original = controls.read_text()
        assert '<!-- harness:control-map=minimum -->' in original
        controls.write_text(original + '\n<PROJECT>\n')
        check('unresolved <PROJECT>')
        controls.write_text(original + '\n[Missing evidence](SPEC.md#missing-evidence)\n')
        check('missing anchor')
        controls.write_text(original)
        # The optional subsystem becomes part of the reachable graph only on use.
        subsystem = root / 'docs/orders.md'
        assert subsystem.exists(), 'the shipped subsystem template must be exercised'
        workflow = root / 'docs/workflow.md'
        workflow.write_text(workflow.read_text() + '\n[Orders runtime](orders.md)\n')
        check()
        # Rendered is not necessarily routed: each selected template must cause
        # a behaviour failure when left unfinished, including future additions.
        for doc in rendered:
            text = doc.read_text()
            try:
                doc.write_text(text + '\n<PROJECT>\n')
                check(f'{doc.relative_to(root)}: unresolved <PROJECT>')
            finally:
                doc.write_text(text)
        (root / 'src/orders.py').unlink()
        check('broken link')
        (root / 'src/orders.py').write_text('def create_order(payload):\n    return payload\n')
        # A real product selection can omit optional docs after removing their links.
        omitted = {'glossary.md', 'roadmap.md', 'data-contracts.md', 'deps-and-configs.md'}
        for doc in root.rglob('*.md'):
            if doc.name != '_template.md':
                doc.write_text(''.join(line for line in doc.read_text().splitlines(keepends=True)
                                       if not any(f']({n})' in line or f'](docs/{n})' in line for n in omitted)))
        for filename in omitted:
            (root / 'docs' / filename).unlink()
        workflow.write_text(workflow.read_text().replace('\n[Orders runtime](orders.md)\n', '\n'))
        subsystem.unlink()
        check()
        # No-link comments remain legal; a genuine token inside a comment still fails.
        controls.write_text(controls.read_text() + '\n<!-- maintainer note -->\n')
        check()
        controls.write_text(controls.read_text() + '\n<!-- owner: <OWNER> -->\n')
        check('unresolved <OWNER>')
    print(f'PASS: {count} full product / pruned product / marker / evidence / source-link probes')


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
    product_probes()


if __name__ == '__main__':
    main()
