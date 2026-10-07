# SentinelZone SIEM Backend release manifest

| Field | Value |
|---|---|
| Project/component | SentinelZone SOC Platform — SIEM Backend |
| Standalone repository | SentinelZone-SIEM-Backend |
| Version | 0.28.1 |
| Creation date (UTC) | 2026-10-07 |
| Python used to build/validate | 3.12.14 |
| Migration head | 0003 (published history unchanged) |
| API paths / operations | 36 / 40 |
| Pytest (standalone source acceptance) | 179 passed / 0 failed / 2 skipped |
| Acceptance | PASS — all 23 local categories/checks; reports/acceptance-summary.json |
| Module imports | PASS — 71 application modules |
| Security scan | PASS — source heuristic scanner and reviewed credential/artifact patterns |
| Source preservation | PASS — app, tests, migrations, contracts, fixtures, deployment, dependencies and stored OpenAPI unchanged from prepared handoff |
| PostgreSQL live status | UNVERIFIED |
| Connector/provider live status | Splunk, Wazuh, CryptoGuard, Telegram, SMS: UNVERIFIED |
| Target-host deployment | Docker, nginx, systemd: UNVERIFIED |
| GitHub-hosted Actions | UNVERIFIED; root workflow/static checks and local SQLite equivalent only |
| ZIP regular-file count | 182 |
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
| MODIFIED | `.github/workflows/backend-ci.yml` |
| MODIFIED | `CHANGELOG.md` |
| MODIFIED | `CONTRIBUTING.md` |
| MODIFIED | `INSTALL.md` |
| MODIFIED | `LICENSE-TODO.md` |
| MODIFIED | `PUSH_TO_GITHUB.md` |
| MODIFIED | `README.md` |
| MODIFIED | `RELEASE_MANIFEST.md` |
| MODIFIED | `SECURITY.md` |
| MODIFIED | `SHA256SUMS` |
| MODIFIED | `TESTING.md` |
| MODIFIED | `docs/CONFIGURATION.md` |
| MODIFIED | `docs/DEPENDENCY_LICENSES.md` |
| MODIFIED | `docs/INTEGRATION.md` |
| MODIFIED | `docs/KNOWN_LIMITATIONS.md` |
| MODIFIED | `docs/QUICKSTART.md` |
| MODIFIED | `docs/RELEASE_NOTES.md` |
| MODIFIED | `docs/STATUS.md` |
| MODIFIED | `reports/README.md` |
| MODIFIED | `reports/SHA256SUMS` |
| MODIFIED | `reports/acceptance-output.txt` |
| MODIFIED | `reports/acceptance-tests.xml` |
| MODIFIED | `reports/changed-files.txt` |
| MODIFIED | `reports/production-validation.xml` |
| MODIFIED | `reports/runtime-smoke.json` |
| ADDED | `reports/standalone-validation.json` |
| MODIFIED | `scripts/build-release.py` |
| MODIFIED | `scripts/validate_release.py` |

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
