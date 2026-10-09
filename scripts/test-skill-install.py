#!/usr/bin/env python3
"""Probe staging, symlink preservation, source validation and rollback in owned temps."""
import importlib.util
from pathlib import Path
import shutil
import tempfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('installer', ROOT / 'scripts/install-skill.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


def main():
    with tempfile.TemporaryDirectory(prefix='harness-install-') as name:
        base = Path(name).resolve()
        agents = base / 'agents/skills'
        claude = base / 'claude/skills'
        agents.mkdir(parents=True)
        claude.mkdir(parents=True)
        target = agents / installer.NAME
        target.mkdir()
        (target / 'local-patch.md').write_text('preserve in backup')
        (target / 'SKILL.md').write_text('---\nname: harness-framework\n---\nold skill\n')
        alias = claude / installer.NAME
        alias.symlink_to(target, target_is_directory=True)
        installer.install(ROOT, [alias, target])
        assert alias.is_symlink() and alias.resolve() == target
        backups = list((agents.parent / 'skill-backups').iterdir())
        assert len(backups) == 1 and (backups[0] / 'local-patch.md').read_text() == 'preserve in backup'
        assert installer.install(ROOT, [alias, target], check=True) == 0
        (target / 'extra-runtime.md').write_text('detect extra')
        assert installer.install(ROOT, [alias, target], check=True) == 1
        (target / 'extra-runtime.md').unlink()
        (target / 'SKILL.md').write_text('---\nname: harness-framework\n---\nlocal drift\n')
        assert installer.install(ROOT, [alias, target], check=True) == 1
        second = base / 'second/skills'
        second.mkdir(parents=True)
        second_target = second / installer.NAME
        second_target.mkdir()
        (second_target / 'old.md').write_text('second prior')
        (second_target / 'SKILL.md').write_text('---\nname: harness-framework\n---\n')
        replace = installer.os.replace
        def fail_second_swap(src, dst):
            if Path(src).name.startswith('.harness-framework-stage-') and Path(dst) == second_target:
                raise OSError('injected second swap failure')
            return replace(src, dst)
        try:
            with patch.object(installer.os, 'replace', side_effect=fail_second_swap):
                installer.install(ROOT, [target, second_target])
        except OSError:
            pass
        else:
            raise AssertionError('expected swap failure')
        assert (target / 'SKILL.md').read_text() == '---\nname: harness-framework\n---\nlocal drift\n'
        assert (second_target / 'old.md').read_text() == 'second prior'
        assert alias.is_symlink()
        assert not list(agents.glob('.harness-framework-stage-*'))
        assert installer.install(ROOT, [ROOT], check=True) == 0
        try:
            installer.install(ROOT, [base / 'missing/skills' / installer.NAME])
        except ValueError as exc:
            assert 'no available' in str(exc)
        else:
            raise AssertionError('all skipped must fail')
        unrelated = base / 'unrelated-project'
        unrelated.mkdir()
        (unrelated / '.git').mkdir()
        (unrelated / 'important.txt').write_text('untouched')
        malicious_alias = second / 'unsafe-alias'
        malicious_alias.symlink_to(unrelated, target_is_directory=True)
        try:
            installer.install(ROOT, [malicious_alias])
        except ValueError as exc:
            assert 'Git worktree' in str(exc)
        else:
            raise AssertionError('unrelated worktree must not be replaced')
        assert (unrelated / 'important.txt').read_text() == 'untouched'
        (unrelated / '.git').rmdir()
        try:
            installer.install(ROOT, [malicious_alias])
        except ValueError as exc:
            assert 'recognized' in str(exc)
        else:
            raise AssertionError('unrecognized user directory must not be replaced')
        assert (unrelated / 'important.txt').read_text() == 'untouched'
        # Missing source resource is rejected before any target mutation.
        source = base / 'broken-source'
        source.mkdir()
        for resource in installer.RESOURCES:
            path = ROOT / resource
            if resource == 'templates':
                continue
            dest = source / resource
            if path.is_file():
                shutil.copy2(path, dest)
            else:
                dest.mkdir()
        try:
            installer.install(source, [target])
        except ValueError as exc:
            assert 'missing source resource' in str(exc)
        else:
            raise AssertionError('broken source must fail')
        assert (target / 'SKILL.md').read_text() == '---\nname: harness-framework\n---\nlocal drift\n'
    print('PASS: install / shared alias / backup / hash drift / multi-target rollback / missing source / all-skipped probes')


if __name__ == '__main__':
    main()
