"""Handoff safety regressions; synthetic markers only, no real credentials."""
import importlib.util
from pathlib import Path
import subprocess
import sys

import pytest

from scripts.check_secrets import scan_blob, scan_tree

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize('name', ['.env.production', 'identity.pfx', 'identity.p12', 'backup.sqlite', 'events.db-wal'])
def test_release_rejects_private_artifacts(tmp_path, name):
    sys.path.insert(0, str(ROOT/'scripts'))
    try:
        spec = importlib.util.spec_from_file_location('release_builder', ROOT/'scripts/build-release.py')
        builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(builder)
    finally:
        sys.path.pop(0)
    (tmp_path/name).write_text('synthetic artifact')
    assert scan_tree(tmp_path)
    with pytest.raises(ValueError, match='private/runtime'):
        builder.files(tmp_path)


def test_scan_reports_location_without_disclosing_marker():
    marker = 'gh' + 'p_' + 'A'*36
    findings = scan_blob(Path('config.txt'), marker.encode())
    assert findings and 'config.txt:1:' in findings[0]
    assert marker not in '\n'.join(findings)
    assert not scan_blob(Path('.env.example'), b'POSTGRES_PASSWORD=\n')


def test_staged_scan_reads_index_not_cleaned_working_file(tmp_path):
    # A clean working tree file must not hide the older secret still staged in Git.
    subprocess.run(['git', 'init', '-q', str(tmp_path)], check=True)
    marker = 'gh' + 'p_' + 'B'*36
    target = tmp_path/'config.txt'
    target.write_text(marker)
    subprocess.run(['git', 'add', 'config.txt'], cwd=tmp_path, check=True)
    target.write_text('clean working copy')
    result = subprocess.run([sys.executable, str(ROOT/'scripts/check_secrets.py'), '--staged'],
                            cwd=tmp_path, capture_output=True, text=True)
    assert result.returncode == 1 and 'config.txt:1:' in result.stdout
    assert marker not in result.stdout + result.stderr
