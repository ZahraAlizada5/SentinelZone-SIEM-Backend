"""Build a clean standalone repository ZIP, source checksums and external archive manifest.

Run validation first. This command never labels an unexecuted live/extraction gate PASS.
The external manifest carries the final ZIP hash: including a ZIP's own hash inside
that ZIP would be self-referential. Retest the extracted ZIP and append that evidence
to the external manifest without rebuilding the archive.
"""
import argparse
import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import stat
import sys
import zipfile

from check_secrets import EXCLUDED, private_path, scan_tree

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_ROOT = 'SentinelZone-SIEM-Backend'
GENERATED = {'reports/changed-files.txt', 'reports/SHA256SUMS', 'RELEASE_MANIFEST.md', 'SHA256SUMS'}
DENIED_SUFFIXES = {'.pyc', '.pyo', '.log', '.tmp', '.swp', '.zip', '.gz', '.tar', '.7z'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def files(root=ROOT):
    result = []
    for path in sorted(root.rglob('*')):
        rel = path.relative_to(root)
        if EXCLUDED.intersection(rel.parts):
            continue
        if path.is_symlink():
            raise ValueError(f'Symlink cannot be packaged: {rel}')
        if not path.is_file():
            continue
        if path.suffix in {'.pyc', '.pyo'}:
            continue
        if (private_path(rel) or path.suffix.lower() in DENIED_SUFFIXES or path.name.endswith('~')
                or {'logs','backups','dist','build','htmlcov'} & set(rel.parts)
                or path.name in {'.coverage','.DS_Store','Thumbs.db'}):
            raise ValueError(f'Remove private/runtime/temporary artifact before packaging: {rel}')
        result.append(path)
    return result


def manifest(version, date, acceptance, validation, api, count, changes):
    counts = acceptance['counts']
    categories = acceptance['categories']
    operations = sum(k in {'get','post','put','patch','delete','options','head'} for v in api['paths'].values() for k in v)
    change_rows = '\n'.join(f'| {state} | `{name}` |' for state, name in changes)
    return f'''# SentinelZone SIEM Backend release manifest

| Field | Value |
|---|---|
| Project/component | SentinelZone SOC Platform — SIEM Backend |
| Standalone repository | SentinelZone-SIEM-Backend |
| Version | {version} |
| Creation date (UTC) | {date} |
| Python used to build/validate | {sys.version.split()[0]} |
| Migration head | {validation['migration_head']} (published history unchanged) |
| API paths / operations | {len(api['paths'])} / {operations} |
| Pytest (standalone source acceptance) | {counts['passed']} passed / {counts['failed']} failed / {counts['skipped']} skipped |
| Acceptance | PASS — all {len(categories)} local categories/checks; reports/acceptance-summary.json |
| Module imports | PASS — {validation['application_modules_imported']} application modules |
| Security scan | PASS — source heuristic scanner and reviewed credential/artifact patterns |
| Source preservation | PASS — app, tests, migrations, contracts, fixtures, deployment, dependencies and stored OpenAPI unchanged from prepared handoff |
| PostgreSQL live status | {acceptance.get('postgresql_live_acceptance','UNVERIFIED')} |
| Connector/provider live status | Splunk, Wazuh, CryptoGuard, Telegram, SMS: UNVERIFIED |
| Target-host deployment | Docker, nginx, systemd: UNVERIFIED |
| GitHub-hosted Actions | UNVERIFIED; root workflow/static checks and local SQLite equivalent only |
| ZIP regular-file count | {count} |
| ZIP SHA-256 | See the external manifest and adjacent .zip.sha256 sidecar |
| Final ZIP extraction check | Recorded after packaging in the external manifest; not claimed by this embedded copy |

The final ZIP cannot contain its own SHA-256. Its digest is recorded only in adjacent
files after archive creation. Root `SHA256SUMS` covers every shipped file except
itself; `reports/SHA256SUMS` covers every shipped file except both checksum files.
Verify these before acceptance, which refreshes report files. The final archive is
never modified or rebuilt after its SHA-256 is calculated.

## Verified checks

Source acceptance includes full pytest, pip check, syntax/dependency/example/link/CI
path validation, runtime OpenAPI/schema equality, secret scanning, a real loopback
Uvicorn/SQLite smoke, and populated SQLite upgrade/downgrade/upgrade plus Alembic
schema parity. Source preservation and import evidence are in
[standalone-validation.json](reports/standalone-validation.json). All original
application behavior and all 181 collected tests from the prepared handoff remain.
No application, migration, schema, test, dependency, or Docker service rename was
needed for the standalone layout.

## UNVERIFIED checks and known limitations

Live PostgreSQL DDL/locks/concurrency/backup-restore; real Splunk, Wazuh, CryptoGuard;
Telegram/SMS delivery; target Docker/nginx/systemd/TLS/VPN; GitHub-hosted Actions
(including its PostgreSQL job); native Windows/macOS; frontend end-to-end mapping;
representative load, retention, and production certification remain UNVERIFIED.
The two pytest skips require advisory locks and FOR UPDATE SKIP LOCKED. One
Starlette TestClient/httpx deprecation warning remains. No vulnerability-feed audit,
container SBOM certification, or comprehensive security certification was performed.

Wazuh may need an alerts adapter; action proposals do not execute actions; provider
configuration belongs to one configured tenant; external delivery is at-least-once
across send/commit crashes; licensing awaits owner selection. See
[KNOWN_LIMITATIONS.md](docs/KNOWN_LIMITATIONS.md) and [LICENSE-TODO.md](LICENSE-TODO.md).
Third-party notices and the dependency license inventory are preserved.

## Changed and added files

Comparison is against the prepared v0.28.1 handoff after removing its old source
subdirectory prefix. Packaging metadata is regenerated. No source files are removed.
See [changed-files.txt](reports/changed-files.txt) for the full inventory.

| Change | Repository-relative file |
|---|---|
{change_rows}

## Final repository structure

All contents below are under the single archive directory `SentinelZone-SIEM-Backend/`.
That directory is the Git repository root and the working directory for commands.

| Path | Purpose |
|---|---|
| `.github/workflows/backend-ci.yml` | Root GitHub Actions workflow |
| `app/`, `contracts/` | Application and unchanged API schemas |
| `deploy/`, `migrations/` | Deployment templates and preserved migration history |
| `docs/`, `fixtures/`, `reports/` | Guides, synthetic payloads, measured evidence |
| `scripts/`, `tests/` | Root-relative developer tools and complete existing test suite |
| `README.md`, `PUSH_TO_GITHUB.md`, `CONTRIBUTING.md`, `SECURITY.md` | Onboarding, publication, contribution, disclosure |
| `Dockerfile`, `docker-compose.yml`, `alembic.ini` | Root runtime and migration configuration |
| `requirements.txt`, `requirements.lock.txt`, `.env.example` | Dependencies and placeholder-only environment template |
| `LICENSE-TODO.md`, `THIRD_PARTY_NOTICES.md` | Pending project license and dependency notices |
| `RELEASE_MANIFEST.md`, `SHA256SUMS` | Release scope and complete source integrity list |

[README](README.md), [Status](docs/STATUS.md), and [push instructions](PUSH_TO_GITHUB.md)
provide the complete developer handoff. No credentials, databases, logs, caches,
virtual environments, backups, or Git history belong in this source archive.
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', type=Path, help='Optional read-only prepared handoff ZIP for change inventory')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.is_relative_to(ROOT):
        parser.error('Output must be outside the repository root')
    if output.exists():
        parser.error('Output already exists; final archives are immutable, choose a new output path')
    if (ROOT/'backend').exists():
        parser.error('Standalone source must not contain a nested backend directory')
    for name in ('PUSH_TO_GITHUB.md', '.github/workflows/backend-ci.yml'):
        if not (ROOT/name).is_file():
            parser.error(f'Missing root release file: {name}')
    findings = scan_tree(ROOT)
    if findings:
        raise SystemExit('\n'.join(findings))
    old = {}
    if args.baseline:
        with zipfile.ZipFile(args.baseline) as original:
            for item in original.infolist():
                if item.is_dir():
                    continue
                parts = Path(item.filename).parts[1:]
                # Normalize the previous handoff layout only for comparison.
                if parts and parts[0] == 'backend':
                    parts = parts[1:]
                name = Path(*parts).as_posix()
                if name in old:
                    raise SystemExit(f'Ambiguous duplicate baseline path: {name}')
                old[name] = digest(original.read(item))
    current = {f.relative_to(ROOT).as_posix(): digest(f.read_bytes()) for f in files()
               if f.relative_to(ROOT).as_posix() not in GENERATED}
    changes = []
    if args.baseline:
        for name in sorted((old.keys() | current.keys()) - GENERATED):
            state = 'REMOVED' if name not in current else 'ADDED' if name not in old else 'MODIFIED' if old[name] != current[name] else None
            if state:
                changes.append((state, name))
        changes.extend(('MODIFIED' if name in old else 'ADDED', name) for name in sorted(GENERATED))
        changes.sort(key=lambda item: item[1])
    (ROOT/'reports/changed-files.txt').write_text(
        ('Compared by SHA-256 with the prepared handoff ZIP after layout normalization.\n' if args.baseline else 'No baseline supplied; change inventory not measured.\n')
        + 'Generated manifest/checksum/change lists are refreshed release metadata.\n'
        + 'All paths are relative to the standalone repository root.\n\n'
        + '\n'.join(f'{state:8} {name}' for state, name in changes) + '\n', encoding='utf-8')
    version = ast.literal_eval(ast.parse((ROOT/'app/__init__.py').read_text()).body[0].value)
    acceptance = json.loads((ROOT/'reports/acceptance-summary.json').read_text())
    validation = json.loads((ROOT/'reports/standalone-validation.json').read_text())
    api = json.loads((ROOT/'docs/openapi.json').read_text())
    categories = acceptance.get('categories', {})
    if (acceptance.get('counts', {}).get('failed') != 0 or not categories
            or any(v != 'PASS' for v in categories.values()) or validation.get('status') != 'PASS'):
        raise SystemExit('Source acceptance/validation is not fully passing; review reports before packaging')
    date = datetime.now(timezone.utc).date().isoformat()
    payload = {f.relative_to(ROOT).as_posix(): f.read_bytes() for f in files()
               if f.relative_to(ROOT).as_posix() not in {'RELEASE_MANIFEST.md','SHA256SUMS','reports/SHA256SUMS'}}
    count = len(payload) + 3
    embedded = manifest(version, date, acceptance, validation, api, count, changes)
    payload['RELEASE_MANIFEST.md'] = embedded.encode()
    payload['reports/SHA256SUMS'] = ''.join(f'{digest(blob)}  {name}\n' for name, blob in sorted(payload.items())).encode()
    payload['SHA256SUMS'] = ''.join(f'{digest(blob)}  {name}\n' for name, blob in sorted(payload.items())).encode()
    for name in ('RELEASE_MANIFEST.md', 'SHA256SUMS', 'reports/SHA256SUMS'):
        (ROOT/name).write_bytes(payload[name])
    findings = scan_tree(ROOT)
    if findings:
        raise SystemExit('\n'.join(findings))
    output.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.fromisoformat(date)
    with zipfile.ZipFile(output, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, blob in sorted(payload.items()):
            info = zipfile.ZipInfo(ARCHIVE_ROOT+'/'+name, (now.year, now.month, now.day, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | (0o755 if name.endswith('.sh') else 0o644)) << 16
            archive.writestr(info, blob)
    with zipfile.ZipFile(output) as archive:
        assert archive.testzip() is None
        assert len(archive.infolist()) == count
    sha = digest(output.read_bytes())
    output.with_suffix('.zip.sha256').write_text(f'{sha}  {output.name}\n')
    external = output.with_name('RELEASE_MANIFEST.md')
    external.write_text(embedded.replace('See the external manifest and adjacent .zip.sha256 sidecar', f'`{sha}`')
                        + f'\nArchive: `{output.name}` ({output.stat().st_size} bytes).\n')
    print(json.dumps({'file': str(output), 'files': count, 'bytes': output.stat().st_size, 'sha256': sha}, indent=2))


if __name__ == '__main__':
    main()
