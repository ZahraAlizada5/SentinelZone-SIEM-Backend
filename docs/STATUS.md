# Release status — 0.28.1

Date: 2026-10-07. Scope: the prepared v0.28.1 handoff converted to the standalone SentinelZone-SIEM-Backend repository without functional changes. Linux / CPython **3.12.14**, exact locked dependencies. This is local acceptance evidence, not a production-readiness certification.

## Measured results

| Check | Result | Evidence / scope |
|---|---|---|
| Supplied baseline reproduced | PASS — 172 passed / 0 failed / 2 skipped | Before handoff edits; original summary retained in reports/baseline-v0.28.0.json |
| Current full pytest suite | **PASS — 179 passed / 0 failed / 2 skipped** | reports/acceptance-tests.xml; includes seven inherited release-tooling cases |
| Acceptance suite | **PASS — all 23 local categories/checks** | reports/acceptance-summary.json and acceptance-output.txt |
| Production regression module | PASS — 58 passed / 0 failed | reports/production-validation.xml |
| Dependency install and consistency | PASS | Clean venv, exact lock installed; pip check; direct requirements + extras dry run required no additional packages on Linux |
| Application imports | PASS — 71 Python modules | Imported from final release source without provider calls |
| Syntax/static docs/config checks | PASS | reports/static-validation.json; Markdown local-file links, lock/requirements, .env.example, Docker paths/Compose YAML |
| Stored OpenAPI/runtime contract | PASS — 36 paths / 40 HTTP operations | Runtime OpenAPI and JSON schemas match; all stored contracts are unchanged from the prepared handoff |
| Migration source head | **0003** | alembic heads; all supplied migration/frozen-schema files unchanged |
| SQLite migration/data/schema parity | PASS | Populated 0002→0003→0002→0003; identity/mode preservation, constraints and Alembic check |
| Native onboarding commands | PASS with temporary SQLite | Alembic upgrade, CLI create-user, authenticated alerts 200 and missing-token 401; reports/developer-smoke.json |
| Real loopback Uvicorn HTTP | PASS | Temporary SQLite; /health 200/degraded, unauthenticated alerts 401, default mocks 404, OpenAPI equality |
| Source secret scan | PASS, heuristic | Known token/key patterns and private artifact paths; values never printed |
| Manual credential/path review | PASS within reviewed source | Only known invalid test markers/redacted fixture values; no required author-machine path |
| Original behavior preservation | PASS | All application, test, migration, contract, fixture, deployment and dependency files byte-identical to the prepared handoff; reports/standalone-validation.json |
| Final ZIP clean extraction | See external RELEASE_MANIFEST.md | Executed after the ZIP is created; that archive is not rebuilt afterward |
| PostgreSQL technical acceptance | **UNVERIFIED** | No installed server/client or Docker runtime; two PostgreSQL-only skips |
| Live connector/provider acceptance | **UNVERIFIED** | No real upstream credentials or provider messages used |
| Docker/nginx/systemd target-host execution | **UNVERIFIED** | Static inspection only; missing Docker/nginx binaries |
| GitHub-hosted workflow | **UNVERIFIED** | Standalone root workflow supplied; YAML/root/cache paths checked; local SQLite equivalent passed |
| Native Windows/macOS | **UNVERIFIED** | Platform markers improved; no native target execution |

## Capability and validation matrix

IMPLEMENTED describes source support. VERIFIED denotes measured execution in the stated column. UNVERIFIED is not BROKEN. A dash means the check is not applicable to that particular capability, not that a live gate passed.

| Capability | Implemented | Verified locally | Verified with SQLite | Requires PostgreSQL acceptance | Requires live lab/target | Remaining unverified scope |
|---|---|---|---|---|---|---|
| API / RBAC / tenant and mode isolation | IMPLEMENTED | VERIFIED | VERIFIED | Yes, database constraints/concurrency | Frontend mapping | PostgreSQL and frontend |
| Normalization / dedup / collector evidence | IMPLEMENTED | VERIFIED with fixtures/mocks | VERIFIED | Yes for production ingestion | Yes | Real data and provider completeness |
| Incident correlation/lifecycle | IMPLEMENTED | VERIFIED | VERIFIED | Yes | Representative load | PostgreSQL/load |
| Case Pack / Replay / What Changed | IMPLEMENTED, documented scope | VERIFIED | VERIFIED | Persistence in production | Real inventory feed | Production scale/feed |
| Assets / metrics / telemetry health | IMPLEMENTED | VERIFIED | VERIFIED | Yes | Real cadence/source timestamps | Liveness acceptance |
| Notification outbox / policy / retry | IMPLEMENTED | VERIFIED with mocks | VERIFIED | SKIP LOCKED/transactions | Telegram/SMS canary | External delivery/concurrency |
| Advisory ingest lock | IMPLEMENTED | UNVERIFIED | — | Yes; skipped locally | Target workers | Real lock exclusion |
| Migration head 0003 | IMPLEMENTED | VERIFIED on SQLite | VERIFIED | Yes | Representative backup/rehearsal | PostgreSQL DDL/duration |
| Splunk connector | IMPLEMENTED | VERIFIED with mocks | Ingest regression | Shared persistence gate | Yes | Live Splunk |
| Wazuh connector | PARTIAL adapter contract | VERIFIED with mocks | Ingest regression | Shared persistence gate | Yes | Actual alert provider/adapter |
| CryptoGuard connector | IMPLEMENTED | VERIFIED with mocks | Ingest regression | Shared persistence gate | Yes | Live telemetry contract |
| Action proposals | PARTIAL: decision workflow, no executor | VERIFIED | VERIFIED | Production persistence | Future execution integration | Execution is not implemented |
| Deployment templates | IMPLEMENTED | Static checks VERIFIED | — | Target database | Yes | Docker/nginx/systemd runtime |
| CI / release packaging | IMPLEMENTED | Local tooling VERIFIED | Acceptance VERIFIED | CI PostgreSQL job | GitHub Actions runner | Hosted execution |

## Skips and warnings

- `test_ingest_lock_blocks_second_worker`: PostgreSQL advisory lock required.
- `test_postgresql_outbox_skip_locked`: PostgreSQL `FOR UPDATE SKIP LOCKED` required.
- One Starlette TestClient/httpx deprecation warning; retained and not suppressed.

All 181 collected cases from the prepared handoff remain unchanged (174 original cases and seven previously added release-tooling cases). No test result is inferred from implementation. Source checksums and changed-file inventory are generated at packaging. Final archive integrity and extracted acceptance are recorded externally to avoid a self-referential ZIP checksum and repeated rebuilding.

See [KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md), [TESTING.md](../TESTING.md), [PostgreSQL acceptance](../POSTGRESQL_ACCEPTANCE.md), and [real connector acceptance](../REAL_CONNECTOR_ACCEPTANCE.md).
