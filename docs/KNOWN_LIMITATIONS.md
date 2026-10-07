# Known limitations and open gates

Applies to v0.28.1. UNVERIFIED means a test was not executed against its real target; it is neither a success nor a failure. The source baseline passed 172 tests with two PostgreSQL-only skips before handoff changes.

| Area | Current limitation / required acceptance |
|---|---|
| PostgreSQL | No PostgreSQL server/client binaries or Docker executable were available in this workspace. Live DDL, advisory exclusion, SKIP LOCKED, PostgreSQL backup/restore and concurrency remain UNVERIFIED. SQLite success does not close this gate. Use the guarded runner in [POSTGRESQL_ACCEPTANCE.md](../POSTGRESQL_ACCEPTANCE.md). |
| Splunk | Live TLS, read-only permissions, index/sourcetype mapping, timestamps, count completeness, export limits and evidence references are UNVERIFIED. |
| Wazuh | PARTIAL integration: Manager auth/health plus an alerts-adapter contract. Standard Manager `/alerts` is not assumed; indexer/adapter work may be required. Live retrieval is UNVERIFIED. |
| CryptoGuard | Real endpoint/key/cursor behavior and payload field mapping are UNVERIFIED. |
| Telegram/SMS | No real message was sent. Canary routing, legacy overlap, provider delivery and target recipients remain UNVERIFIED. Outbox delivery is at-least-once across the send/commit crash boundary. |
| Deployment | Docker and nginx executables were absent. Docker build/run, nginx syntax on the target host, TLS, systemd execution, VPN/firewall and proxy peer validation are UNVERIFIED. Static checks do not replace them. |
| CI | Workflow syntax/paths reviewed and equivalent local SQLite acceptance executed; hosted GitHub Actions and its PostgreSQL job have not run. |
| Windows/macOS | Linux/Python 3.12.14 was tested. Windows uvloop/colorama markers were corrected, but native OS installation/runtime remains UNVERIFIED. Full HTTP acceptance uses POSIX inherited socket descriptors; use Linux/WSL2 for it. |
| Multi-tenant integrations | ORM/request data isolation exists; no PostgreSQL RLS or tenant-specific credential store is implemented. One configured tenant owns live connectors/provider recipients. |
| Telemetry/inventory | Heartbeat cadence must reflect a verified feed. No alerts alone does not establish outage. What Changed requires full inventory snapshots; no automatic OS inventory collector is included. |
| Replay | Built-in asset-correlation versions/window variants only. No arbitrary plugin/rule upload engine or representative production-scale load acceptance. |
| Case Pack | Optional users/MITRE/AI references may be empty. Actions performed remain empty because no executor exists. |
| Action proposals | Create/approve/reject/expiry/protected-target workflow only. Approval does not block IPs, disable users or isolate endpoints. |
| Historical data | Mixed REAL/TEST incidents stop migration before changes. Old fixtures mislabeled REAL cannot be identified automatically. Downgrade can lose newer investigation tables and is guarded against key collisions. |
| Frontend | Not included; authenticated `/v1` response mapping and browser behavior need joint integration testing. |
| Dependency scope | Original lock retains optional FastAPI CLI/transitive packages. No dependency vulnerability feed audit, wheel reproducibility/hash lock, or container SBOM certification was performed. License inventory records package metadata, not legal clearance. |
| Licensing | No original project license grant was supplied. Standalone packaging preserves LICENSE-TODO.md and does not establish ownership or a reuse grant. Owner selection/rights confirmation is required before unrestricted reuse. |

The baseline/current suite reports a Starlette warning that `httpx` with TestClient is deprecated and suggests `httpx2`. It is not a failure. The current httpx contract and tested dependency versions are preserved; review a future dependency transition separately.

The portable secret scanner recognizes known token/key patterns and private artifact paths. It does not detect every possible credential or scan remote Git history. Manual source review complements it; no comprehensive penetration/security certification is claimed. Synthetic fixture addresses and redacted password markers are test data, not deployment configuration.

Detailed earlier findings remain in [FIX_REPORT.md](../FIX_REPORT.md); actual current results are in [STATUS.md](STATUS.md). There are no intentionally hidden test failures.
