# SentinelZone SIEM Backend 0.28.1

Date: 2026-10-07. This is the standalone packaging of the prepared v0.28.1 developer handoff. Extract the ZIP and open `SentinelZone-SIEM-Backend/`; that directory is the complete repository root. No additional restructuring is needed.

## Standalone changes

- Moved the complete component and handoff files into one repository root, including `.github/workflows/backend-ci.yml`.
- Updated README, quick start, configuration, testing, contribution, security, release, and GitHub publication instructions for the standalone layout.
- Updated CI working paths and dependency-cache paths; retained both isolated SQLite and disposable PostgreSQL jobs.
- Updated source validation and archive generation for root-relative paths, immutable final archive creation, checksums, and a measured change inventory.
- Preserved application source, all 181 collected tests, migrations, contracts/OpenAPI, fixtures, deployment configurations, and exact dependency versions byte-for-byte from the prepared handoff.
- Preserved LICENSE-TODO.md and third-party notices; corrected the dependency inventory's swapped column headings.

## Compatibility and installation

Python 3.12; PostgreSQL via psycopg for production; Alembic head `0003`; 36 API paths and 40 operations. Version remains 0.28.1. No new migration, schema, endpoint, or business behavior is introduced. Read [Quick start](QUICKSTART.md), and back up before upgrading an existing deployment. The Docker Compose service is still named `backend`; this is a service name, not a required source subdirectory.

## Evidence and open gates

The full standalone source suite measures **179 passed / 0 failed / 2 skipped**; all **23 local acceptance categories/checks** pass. See [Status](STATUS.md), [Known limitations](KNOWN_LIMITATIONS.md), and the measured reports. The two skips require PostgreSQL advisory locks and SKIP LOCKED. The exact final ZIP is extracted and retested after creation; those results and its SHA-256 are recorded in the adjacent external release manifest without rebuilding the archive.

Real PostgreSQL, Splunk, Wazuh, CryptoGuard, Telegram/SMS, target Docker/nginx/systemd, frontend end-to-end mapping, and hosted GitHub Actions remain UNVERIFIED. Mocked/local success is not live acceptance.

No original-code license is invented. [LICENSE-TODO.md](../LICENSE-TODO.md) must be resolved by the owner before unrestricted reuse. The separate final integration repository is not the publication destination for this standalone component.
