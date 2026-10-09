#!/usr/bin/env python3
"""Real Gate replay plus illustrative lifecycle / retrieval probes; no model A/B."""
from pathlib import Path
import subprocess
import re
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def probe(script, project, status, diagnostic):
    result = subprocess.run(['bash', str(script)], cwd=project, text=True, capture_output=True)
    assert result.returncode == status, (result.returncode, result.stdout, result.stderr)
    assert diagnostic in result.stdout + result.stderr, (diagnostic, result.stdout, result.stderr)


def load_record():
    rows = [line.strip().strip('|').split('|') for line in (HERE / 'index.md').read_text().splitlines() if line.startswith('| EXP-GATE-001 |')]
    assert len(rows) == 1, 'experience ID must have exactly one index row'
    identifier, state, triggers, excluded, link = [column.strip() for column in rows[0]]
    target = re.search(r'\]\(([^)]+)\)', link)
    assert target, 'index must link to the evidence entry'
    entry_path = (HERE / target[1]).resolve()
    assert entry_path.is_relative_to(HERE) and entry_path.is_file(), 'entry link must resolve inside this sample'
    entry = entry_path.read_text()
    assert entry.startswith(f'# {identifier}'), 'index ID must match entry'
    assert f'- 状态：{state}；' in entry, 'index and entry state drift'
    assert state in {'candidate', 'evaluated', 'active', 'retired', 'rejected'}, 'unknown state'
    return {'state': state, 'triggers': {x.strip() for x in triggers.split(',')},
            'excluded': {x.strip() for x in excluded.split(',')}}


def recalled(record, task, purpose='execution'):
    if task in record['excluded'] or task not in record['triggers']:
        return False
    if record['state'] == 'active':
        return True
    return purpose == 'maintenance-evaluation' and record['state'] in {'candidate', 'evaluated'}


def promote(state, evaluation_passed, authorized):
    if state != 'evaluated' or not evaluation_passed or not authorized:
        raise ValueError('evaluation and corresponding authority are required')
    return 'active'


def main():
    with tempfile.TemporaryDirectory(prefix='harness-replay-') as name:
        project = Path(name)
        (project / 'scripts').mkdir()
        for folder in ('domain', 'services', 'routes'):
            (project / 'src' / folder).mkdir(parents=True)
        old = (HERE / 'fixtures/pre-2.3-check-redlines.sh').read_text()
        new = (ROOT / 'examples/node-orders-api/scripts/check-redlines.sh').read_text()
        old_script = project / 'scripts/old.sh'
        new_script = project / 'scripts/new.sh'
        def bad_regex(source):
            return '\n'.join('check "R1" "bad regex" "[" src/domain' if line.startswith('check "R1"') else line for line in source.splitlines()) + '\n'
        old_script.write_text(bad_regex(old))
        new_script.write_text(bad_regex(new))
        probe(old_script, project, 0, '红线全部清零')
        probe(new_script, project, 2, 'ERROR [R1]')
        print('REPLAY: invalid regex: old=PASS (escape), new=ERROR (blocked)')
        new_script.write_text(new)
        (project / 'src/domain/legal.ts').write_text('export const id: string = "order-1"\n')
        probe(new_script, project, 0, 'PASS')
        (project / 'src/domain/violation.ts').write_text("import x from '@prisma/client'\n")
        probe(new_script, project, 1, 'FAIL [R1]')
    record = load_record()
    assert record['state'] == 'active', 'published sample should be active'
    assert {'ui-copy', 'ordinary-business'} <= record['excluded'], 'exclusion scope drift'
    for excluded in record['excluded']:
        assert not recalled({**record, 'triggers': record['triggers'] | {excluded}}, excluded), 'exclusion must win over a broad trigger'
    assert recalled(record, 'gate-maintenance')
    assert recalled(record, 'false-green-audit')
    assert not recalled(record, 'ui-copy')
    assert not recalled(record, 'ordinary-business')
    assert not recalled(record, 'unknown-task')
    # Candidate and retirement cases are explicitly synthetic policy probes.
    assert not recalled({**record, 'state': 'candidate'}, 'gate-maintenance')
    assert recalled({**record, 'state': 'candidate'}, 'gate-maintenance', 'maintenance-evaluation')
    assert recalled({**record, 'state': 'evaluated'}, 'gate-maintenance', 'maintenance-evaluation')
    assert not recalled({**record, 'state': 'retired'}, 'gate-maintenance', 'maintenance-evaluation')
    # Illustrative state history only; no claim the active real record was retired.
    history = ['candidate', 'evaluated', promote('evaluated', True, True), 'retired']
    assert history == ['candidate', 'evaluated', 'active', 'retired']
    for state, passed, authorized in [('candidate', True, True), ('evaluated', False, True), ('evaluated', True, False)]:
        try:
            promote(state, passed, authorized)
        except ValueError:
            continue
        raise AssertionError('unqualified promotion allowed')
    print('PASS: 4 real Gate probes; actual index / entry retrieval and exclusions; illustrative promotion / retirement policy probes')
    print('NOT RUN: model with / without Skill A/B')


if __name__ == '__main__':
    main()
