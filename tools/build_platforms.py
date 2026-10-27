#!/usr/bin/env python3
"""Build portable Commeto packages without network access or dependencies."""
import hashlib
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'plugins/commeto/skills/video-research'


def write_zip(target, entries):
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(entries.items()):
            assert not name.startswith('/') and '..' not in name.split('/')
            entry = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, data)
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None
        assert set(archive.namelist()) == set(entries)


def build():
    manifest = json.loads((ROOT / 'plugins/commeto/plugin.json').read_text())
    version = manifest['version']
    gemini = json.loads((ROOT / 'gemini-extension.json').read_text())
    assert gemini['version'] == version
    assert gemini['name'] == 'commeto'
    assert gemini['contextFileName'] == 'GEMINI.md'
    instructions = (ROOT / 'GEMINI.md').read_bytes()
    assert instructions == (ROOT / 'platforms/gemini/INSTRUCTIONS.md').read_bytes()
    for path in SKILL.rglob('*.md'):
        for link in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            if '://' not in link and not link.startswith('#') and not any(c.isspace() for c in link):
                assert (path.parent / link.split('#')[0]).is_file(), (path, link)
    files = [p for p in SKILL.rglob('*') if p.is_file()
             and '__pycache__' not in p.parts and p.suffix != '.pyc'
             and 'agents' not in p.relative_to(SKILL).parts]
    assert all(not p.is_symlink() for p in files)
    claude_entries = {'video-research/' + p.relative_to(SKILL).as_posix(): p.read_bytes()
                      for p in files}
    claude_entries['video-research/LICENSE'] = (ROOT / 'LICENSE').read_bytes()
    assert 'video-research/SKILL.md' in claude_entries
    assert 'video-research/references/viewer-feedback.md' in claude_entries
    dist = ROOT / 'dist'
    dist.mkdir(exist_ok=True)
    claude = dist / f'commeto-claude-{version}.zip'
    write_zip(claude, claude_entries)
    extension = dist / f'commeto-gemini-cli-{version}.zip'
    write_zip(extension, {name: (ROOT / name).read_bytes()
                          for name in ('gemini-extension.json', 'GEMINI.md', 'LICENSE')})
    gem = dist / f'commeto-gemini-instructions-{version}.txt'
    gem.write_bytes(instructions)
    checksums = dist / 'SHA256SUMS'
    lines = checksums.read_text().splitlines() if checksums.exists() else []
    targets = (claude, extension, gem)
    lines = [line for line in lines if line.split()[-1] not in {p.name for p in targets}]
    for path in targets:
        lines.append(f'{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}')
        print(f'Built {path.name}')
    checksums.write_text('\n'.join(sorted(lines)) + '\n')
    return targets


if __name__ == '__main__':
    build()
