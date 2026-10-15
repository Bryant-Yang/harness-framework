#!/usr/bin/env python3
"""Check instantiated Harness document closure, not project behaviour or authority."""
import argparse
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

DEFAULT_OWNERS = {'direction': 'HARNESS.md', 'workflow': 'docs/workflow.md',
                  'controls': 'docs/harness-controls.md', 'behaviour': 'docs/SPEC.md'}
# Match known framework tokens, not legal TypeScript generic parameters such as <T>.
KNOWN_TOKENS = {'PROJECT', 'AUTHOR', 'MISSION', 'STACK', 'CI_CMD', 'YYYY-MM-DD', 'N', 'M',
                'BASELINE', 'EVIDENCE', 'OWNER', 'CONTROLS', 'SCENE', 'OUTPUT', 'SOURCE_SHA',
                'LOCAL_DELTA', 'LEGACY_STATUS', 'sha', '语言', '...'}
# HTML comments carry contract markers, not fill-in fields. An actual field
# nested inside a comment (<!-- owner: <OWNER> -->) must still be detected.
PLACEHOLDER = re.compile(r'<(?![!/])([^<>\n]+)>')
for template in (Path(__file__).resolve().parents[1] / 'templates').rglob('*.template.md'):
    KNOWN_TOKENS.update(PLACEHOLDER.findall(template.read_text()))

LINK = re.compile(r'(?<!!)\[[^\]\n]*\]\(([^)\n]+)\)')


def slug(heading):
    heading = re.sub(r'\[([^]]+)\]\([^)]+\)', r'\1', heading)
    heading = re.sub(r'<[^>]+>', '', heading).strip().lower()
    return re.sub(r'[^\w\- ]', '', heading).replace(' ', '-')


def anchors(text):
    text = re.sub(r'^```.*?^```\s*$', '', text, flags=re.M | re.S)
    result = set(re.findall(r'<a\s+(?:id|name)=[\'"]([^\'"]+)', text))
    counts = {}
    for heading in re.findall(r'^#{1,6}\s+(.+?)(?:\s+#+)?\s*$', text, re.M):
        key = slug(heading)
        n = counts.get(key, 0)
        counts[key] = n + 1
        result.add(key if not n else f'{key}-{n}')
    return result


def validate(root, profile, legacy, owners):
    root = root.resolve()
    errors = []
    keys = ['direction', 'workflow', 'controls'] + (['behaviour'] if profile == 'product' else [])
    pending = [root / 'AGENTS.md'] + [root / owners[k] for k in keys]
    visited = set()
    legacy_link = False
    while pending:
        doc = pending.pop()
        if doc in visited:
            continue
        visited.add(doc)
        resolved = doc.resolve()
        if not resolved.is_relative_to(root):
            errors.append(f'outside project: {doc}')
            continue
        if not doc.is_file():
            errors.append(f'missing document: {doc.relative_to(root)}')
            continue
        if doc.name == '_template.md':
            continue
        if '.template.' in doc.name:
            errors.append(f'unrenamed template: {doc.relative_to(root)}')
        text = doc.read_text()
        # Fenced code still contains placeholders that must be filled; skip code only for links.
        for token in sorted(set(PLACEHOLDER.findall(text))):
            if token in KNOWN_TOKENS:
                errors.append(f'{doc.relative_to(root)}: unresolved <{token}>')
        linked_text = re.sub(r'^```.*?^```\s*$', '', text, flags=re.M | re.S)
        labels = {raw: label for label, raw in re.findall(r'(?<!!)\[([^\]\n]*)\]\(([^)\n]+)\)', linked_text)}
        for raw in LINK.findall(linked_text):
            link = raw.strip().split(' "', 1)[0].strip('<>')
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc:
                continue
            target = (doc.parent / unquote(parsed.path)).resolve() if parsed.path else resolved
            if not target.is_relative_to(root):
                errors.append(f'{doc.relative_to(root)}: link outside project: {raw}')
                continue
            if not target.exists():
                errors.append(f'{doc.relative_to(root)}: broken link: {raw}')
                continue
            if doc == root / owners['controls'] and re.search(r'baseline|基线', labels.get(raw, ''), re.I) and target.is_file():
                legacy_link = True
            if target.is_file() and target.suffix == '.md':
                if parsed.fragment and unquote(parsed.fragment) not in anchors(target.read_text()):
                    errors.append(f'{doc.relative_to(root)}: missing anchor: {raw}')
                pending.append(target)
    if legacy and not legacy_link:
        errors.append('legacy: Controls must link to an existing approved file with a baseline / 基线 label')
    return errors, len(visited)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    parser.add_argument('--profile', choices=['minimal', 'product'], default='minimal')
    parser.add_argument('--legacy', action='store_true')
    parser.add_argument('--owner', action='append', default=[], metavar='ROLE=PATH')
    args = parser.parse_args()
    owners = dict(DEFAULT_OWNERS)
    for binding in args.owner:
        key, separator, value = binding.partition('=')
        if not separator or key not in owners or not value:
            parser.error(f'invalid owner binding: {binding}')
        owners[key] = value
    try:
        errors, count = validate(args.project, args.profile, args.legacy, owners)
    except (OSError, ValueError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    if errors:
        print('\n'.join(f'FAIL: {x}' for x in errors))
        return 1
    print(f'PASS: {args.profile} document closure ({count} documents); behaviour / routing semantics not evaluated')
    return 0


if __name__ == '__main__':
    sys.exit(main())
