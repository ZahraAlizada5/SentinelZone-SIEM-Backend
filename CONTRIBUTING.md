# Contributing

Contribute to **SentinelZone-SIEM-Backend**, the standalone SIEM component of the SentinelZone SOC Platform. Work from the repository root. Read the [README](README.md), [architecture](ARCHITECTURE.md), [API contract](API.md), and [limitations](docs/KNOWN_LIMITATIONS.md) first. Licensing is pending owner confirmation; contributions must identify provenance and not introduce code you cannot provide.

## Workflow

1. Clone this repository (or your fork) and branch from current `main`. Use `fix/<topic>`, `feat/<topic>`, `docs/<topic>`, or `chore/<topic>`. See [PUSH_TO_GITHUB.md](PUSH_TO_GITHUB.md) for initial repository creation and updates.
2. Create a CPython 3.12 venv and install `requirements.lock.txt`. Keep test checkouts free of deployment `.env` files and real provider credentials.
3. Make a focused change. Preserve route names/response contracts and established transaction, tenant and mode boundaries unless the PR explains a concrete required change.
4. Run `python scripts/acceptance.py`; review counts, warnings and skips. For a database/concurrency change, also run guarded PostgreSQL acceptance on a new disposable database. Live connector checks are separate evidence.
5. Run `python scripts/export_contracts.py --check` and `python scripts/check_secrets.py`. If a contract intentionally changes, regenerate it with `python scripts/export_contracts.py` and review the diff.
6. Review `git diff`, stage only intended files, then run `python scripts/check_secrets.py --staged`. Inspect `git diff --cached --stat` and `git diff --cached` before committing.
7. Commit with a clear message (`fix:`, `feat:`, `docs:`, `test:`, or `chore:`); push the branch and open a PR into `main`.

## Code style and tests

Use four spaces, UTF-8/LF, clear names, and type hints consistent with nearby code. Avoid whole-project reformatting. No formatter/linter gate is retroactively imposed on existing source; `validate_release.py` checks syntax, dependency pins, example safety, links and deployment paths. Add tests that cover the behavior or regression risk, rather than mirroring implementation details. Preserve all existing tests.

Use HTTP mocks/synthetic data in ordinary CI. Never send notifications to real recipients or require Splunk/Wazuh/CryptoGuard access in CI. Never convert a skipped/unexecuted test to PASS. Run ordinary tests without `TEST_DATABASE_URL`; the PostgreSQL acceptance runner requires explicit reset acknowledgement and an empty `*_test` database.

## Migrations and dependency updates

Published revisions and `migrations/schema_0002.py` / `schema_0003.py` are immutable history. Add a new revision for schema changes, include populated upgrade and downgrade/data-preservation tests, review the generated SQL, and rehearse backup/restore on representative data. Do not import current models into frozen historical migrations. Do not silently change `DEFAULT_TENANT_ID` for a populated database.

Update direct requirements and exact lock together in an isolated environment. Verify extras and platform markers, `pip check`, import/static validation, the complete suite, migration parity and generated OpenAPI. Refresh dependency licensing inventory when versions change. A passing local suite does not establish live provider compatibility.

## Pull requests

Describe the problem, resulting behavior, compatibility/migration impact, measured commands/results, skips/open gates, and rollout/rollback needs. Identify relevant docs and contract changes. Do not include real events, tokens, private network details, runtime logs, database dumps or `.env`. Use redacted minimal reproductions. For updates to an existing repository, request review before merging into `main`. Initial publication to a new empty repository follows [PUSH_TO_GITHUB.md](PUSH_TO_GITHUB.md).
