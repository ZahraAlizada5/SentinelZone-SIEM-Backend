# Testing and release acceptance

Use CPython 3.12 in a fresh venv and a clean source checkout with no deployment `.env` or real connector credentials. The exact lock includes SOCKS support. Linux/Python 3.12.14 is the measured platform. On native Windows, ordinary pytest can be run, but the complete acceptance HTTP smoke harness uses POSIX inherited socket descriptors; use WSL2/Linux or CI for full acceptance.

```bash
python -m pip install -r requirements.lock.txt
python -m pip check
python scripts/acceptance.py
```

`bash scripts/acceptance-test.sh` is a compatible POSIX wrapper. Acceptance clears application settings, uses temporary test databases, checks dependencies/secrets/static release/contracts, launches a real loopback Uvicorn process, probes populated migrations, and runs the full pytest suite. It refuses a source checkout containing `.env`. All ordinary connector/provider checks use recorded/synthetic data and HTTP mocks; no real messages are sent.

For individual checks in the same clean checkout:

```bash
python -m pytest -q -ra --junitxml=reports/test-results.xml
python scripts/export_contracts.py --check
python scripts/check_secrets.py
python scripts/validate_release.py
python scripts/runtime-smoke.py
```

`python scripts/check_secrets.py --staged` scans actual Git index blobs, across the entire standalone repository. It works only in a Git checkout; the ordinary source scan also works on an extracted ZIP.

## Results and evidence

[docs/STATUS.md](docs/STATUS.md) contains current measured counts. The supplied v0.28.0 baseline was independently reproduced at **172 passed, 0 failed, 2 skipped** before edits. All original tests remain unchanged. Seven release-tooling cases inherited from the prepared handoff cover private artifact rejection, value-redacted scanner findings, and detection of a secret still staged after its working file has been cleaned.

The two default-suite skips are `test_ingest_lock_blocks_second_worker` (PostgreSQL advisory locks) and `test_postgresql_outbox_skip_locked` (PostgreSQL row locking). SQLite cannot establish those behaviors. A Starlette TestClient/httpx deprecation warning is retained and documented; it is not hidden by a warning filter.

Category statuses are derived from JUnit outcomes. Missing coverage is UNVERIFIED; skips make a category PARTIAL. Source evidence is written under `reports/acceptance-*` and `reports/runtime-smoke.json`. Verify shipped checksums before running the scripts: new runs legitimately replace reports.

## PostgreSQL acceptance — destructive only to a disposable database

Follow [POSTGRESQL_ACCEPTANCE.md](POSTGRESQL_ACCEPTANCE.md). Create a new empty dedicated database ending in `_test`, owned by a test role. The test role needs CREATEDB for the scratch backup/restore drill, and matching `pg_dump`/`pg_restore` binaries must be available (or set `PG_BIN`). These elevated test permissions do not belong on the production runtime role.

Supply `TEST_DATABASE_URL` through a secure environment mechanism; unset any real `DATABASE_URL`. Never use a deployment or shared lab database. Then:

```bash
python scripts/acceptance.py --postgres --allow-test-db-reset
```

The runner refuses absent acknowledgement, an invalid driver/name, a DATABASE_URL collision, or a nonempty DB. It then exercises populated REAL/TEST upgrade/downgrade/upgrade, schema parity, tenant constraints and the full suite, including advisory exclusion, SKIP LOCKED and PostgreSQL backup/restore. It drops application tables inside that explicitly disposable DB. Do not point another service at it.

Any PostgreSQL-mode skip is PARTIAL with a nonzero exit, never full PASS. Migration regression helpers that explicitly use temporary SQLite remain SQLite tests even during this run; the guarded PostgreSQL migration probe is separate and real.

## CI

The workflow already lives at the standalone repository-root path `.github/workflows/backend-ci.yml`. Its checkout, dependency cache, scanners, and commands all use this root. It uses Python 3.12, the lock, source scanning and full acceptance, plus a separate disposable PostgreSQL 16 job with matching client tools. The service has test-only loopback trust and no production credentials; do not reuse that authentication setting in deployment. GitHub-hosted execution is UNVERIFIED in this handoff.

## Release reproduction

From a clean `SentinelZone-SIEM-Backend/` checkout, run acceptance, then write the archive outside the repository:

```bash
python scripts/build-release.py --output ../SentinelZone-SIEM-Backend-v0.28.1.zip
```

Optionally add `--baseline /path/to/original.zip` to regenerate a byte/hash change inventory. The builder rejects private/runtime artifacts and packages repository content under one `SentinelZone-SIEM-Backend/` directory. It refuses to overwrite an existing archive. It emits source checksums, an archive checksum sidecar, and an external manifest. The ZIP's own hash must be outside the ZIP to avoid circular self-hashing.

Extract the actual final ZIP into a clean directory, verify checksums, and rerun `python scripts/acceptance.py` from that extracted repository root. Record those results and the unchanged archive hash in the external manifest. Do not rebuild after this test; any later code/config/doc change requires a newly packaged and extracted validation.
