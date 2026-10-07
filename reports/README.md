# Validation evidence

Reports in this directory are generated locally with synthetic/redacted data. They do not contain a running deployment's logs, database, or provider credentials.

- `baseline-v0.28.0.json`: supplied baseline summary, also reproduced before release edits (172 passed, 2 PostgreSQL skips).
- `acceptance-summary.json`, `acceptance-tests.xml`, `acceptance-output.txt`: current working-source acceptance evidence.
- `runtime-smoke.json`: actual Uvicorn loopback HTTP smoke with a temporary SQLite database; not live connector evidence.
- `developer-smoke.json`: actual Alembic + CLI admin creation + authenticated API read against temporary SQLite; generated credentials discarded.
- `static-validation.json`: syntax, dependency, example, links and deployment-path checks.
- `standalone-validation.json`: measured module imports, migration head, source-preservation hashes, root paths, and runtime availability for this conversion.
- `production-validation.xml`: focused production-config regression evidence.
- `changed-files.txt`: byte/hash difference from the prepared v0.28.1 handoff after normalizing its old layout, generated at packaging.
- `SHA256SUMS`: SHA-256 checksums relative to the repository root, excluding checksum files.

Final clean extraction is tested after archive creation. Its evidence and the ZIP's own SHA-256 are in the **external release manifest** beside the ZIP. The ZIP is not rebuilt after that test. Re-running acceptance writes fresh reports and therefore changes source-file checksums; verify the shipped checksums before running it.
