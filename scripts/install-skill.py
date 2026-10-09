#!/usr/bin/env python3
"""Stage complete Skill resources, preserve shared links and recoverable backups."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
NAME = 'harness-framework'
RESOURCES = ['SKILL.md', 'VERSION', 'README.md', 'LICENSE', 'AI-ADOPTION-PROTOCOL.md',
             'INSTANTIATION-CHECKLIST.md', 'METHODOLOGY.md', 'docs', 'templates', 'examples', 'scripts', 'tests', '.github']
IGNORED = {'.git', 'node_modules', '__pycache__', 'dist', 'coverage', '.DS_Store'}
MANIFEST = '.harness-install.json'


def resource_files(root):
    files = {}
    for resource in RESOURCES:
        path = root / resource
        if not path.exists():
            raise ValueError(f'missing source resource: {resource}')
        candidates = [path] if path.is_file() else sorted(path.rglob('*'))
        for candidate in candidates:
            relative = candidate.relative_to(root)
            if any(part in IGNORED or part.startswith('.smoke-') for part in relative.parts):
                continue
            if candidate.is_symlink():
                raise ValueError(f'source resource must not contain symlink: {relative}')
            if candidate.is_file() and candidate.suffix != '.log':
                files[str(relative)] = candidate
    return files


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_state(root):
    sha = subprocess.run(['git', '-C', str(root), 'rev-parse', 'HEAD'], capture_output=True, text=True)
    if sha.returncode:
        return {'source_commit': None, 'source_dirty': None}
    dirty = subprocess.run(['git', '-C', str(root), 'status', '--porcelain'], capture_output=True, text=True, check=True)
    return {'source_commit': sha.stdout.strip(), 'source_dirty': bool(dirty.stdout)}


def check_target(target, hashes, version):
    problems = []
    for relative, expected in hashes.items():
        path = target / relative
        if not path.is_file() or path.is_symlink() or digest(path) != expected:
            problems.append(relative)
    # Compare the effective file set as well as expected hashes; caches are not resources.
    if target.is_dir():
        for path in target.rglob('*'):
            relative = path.relative_to(target)
            if any(part in IGNORED or part.startswith('.smoke-') for part in relative.parts):
                continue
            if (path.is_file() or path.is_symlink()) and str(relative) not in hashes and str(relative) != MANIFEST:
                problems.append(f'extra:{relative}')
    manifest_path = target / MANIFEST
    try:
        manifest = json.loads(manifest_path.read_text())
        if manifest.get('version') != version or manifest.get('files') != hashes:
            problems.append(MANIFEST)
    except (OSError, ValueError):
        problems.append(MANIFEST)
    return problems


def install(source, targets, check=False):
    source = source.resolve()
    files = resource_files(source)
    hashes = {name: digest(path) for name, path in files.items()}
    version = (source / 'VERSION').read_text().strip()
    manifest = {'version': version, 'files': hashes, **git_state(source)}
    effective = []
    approved_roots = {raw.absolute().parent.resolve() for raw in targets}
    for raw in targets:
        raw = raw.absolute()
        if not raw.parent.is_dir():
            print(f'SKIP: missing parent {raw.parent}')
            continue
        # Resolve existing tool alias before replacing anything; never replace the link itself.
        target = raw.resolve()
        if target == source:
            print(f'PASS: already linked to maintained source: {raw}')
            effective.append((target, True))
            continue
        if source.is_relative_to(target) or target.is_relative_to(source):
            raise ValueError(f'target overlaps maintained source: {raw}')
        if target.exists() and not target.is_dir():
            raise ValueError(f'target is not a directory: {raw}')
        if (target / '.git').exists():
            raise ValueError(f'refusing to replace a Git worktree: {raw}')
        if target.exists():
            entry = target / 'SKILL.md'
            if not entry.is_file() or not re.search(r'^name:\s*harness-framework\s*$', entry.read_text(), re.M):
                raise ValueError(f'target is not a recognized harness-framework Skill: {raw}')
        elif target.parent not in approved_roots:
            raise ValueError(f'new resolved target is outside configured Skill roots: {raw}')
        if (target, False) not in effective:
            effective.append((target, False))
    if not effective:
        raise ValueError('no available install target')
    if check:
        drift = False
        for target, linked in effective:
            if linked:
                continue
            problems = check_target(target, hashes, version)
            if problems:
                print(f'DRIFT: {target}: ' + ', '.join(problems))
                drift = True
            else:
                print(f'PASS: installed {version}, {len(hashes)} file hashes match: {target}')
        return 1 if drift else 0
    staged = []
    moved = []
    try:
        # Stage and validate every destination before the first replacement.
        for target, linked in effective:
            if linked:
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            stage = Path(tempfile.mkdtemp(prefix=f'.{NAME}-stage-', dir=target.parent))
            staged.append((target, stage))
            for relative, path in files.items():
                dest = stage / relative
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, dest)
            (stage / MANIFEST).write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
            if check_target(stage, hashes, version):
                raise ValueError(f'staged package did not verify: {stage}')
        for target, stage in staged:
            backup = None
            if target.exists():
                backup_parent = target.parent.parent / 'skill-backups'
                backup_parent.mkdir(parents=True, exist_ok=True)
                stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
                backup = backup_parent / f'{NAME}-{stamp}'
                os.replace(target, backup)
            moved.append((target, backup))
            os.replace(stage, target)
        for target, backup in moved:
            print(f'INSTALLED: {version}: {target}')
            if backup:
                print(f'BACKUP: {backup}')
        return 0
    except BaseException:
        for target, backup in reversed(moved):
            if target.exists():
                shutil.rmtree(target)
            if backup:
                os.replace(backup, target)
        raise
    finally:
        for _, stage in staged:
            if stage.exists():
                shutil.rmtree(stage)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='read-only version and hash comparison')
    args = parser.parse_args()
    targets = [Path(os.environ.get('CLAUDE_SKILLS_DIR', str(Path.home() / '.claude/skills'))) / NAME,
               Path(os.environ.get('CODEX_SKILLS_DIR', str(Path.home() / '.agents/skills'))) / NAME]
    try:
        return install(ROOT, targets, args.check)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
