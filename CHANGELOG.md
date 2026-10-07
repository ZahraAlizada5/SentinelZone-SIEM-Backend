# Changelog

## 0.28.1 — standalone developer handoff (2026-10-07)

- Flattened the prepared handoff into the standalone `SentinelZone-SIEM-Backend` repository. Updated onboarding, new/existing repository push instructions, contribution/security references, root CI paths, and release tooling.
- The standalone conversion preserves all prepared application, test, migration, contract, fixture, deployment, and dependency files byte-for-byte. No second version bump or functional change is introduced.

The following preparation work was already present in the supplied v0.28.1 handoff and is retained:
- Added English onboarding, configuration, integration, status, limitations, contribution, security, licensing-decision, and dependency-license documentation.
- Preserved all original application behavior, 40 API operations, migration files, fixtures, and tests; only the application/OpenAPI version metadata changed during the earlier v0.28.0 → v0.28.1 preparation, not during standalone conversion.
- Conditioned uvloop for supported platforms, pinned Windows colorama, and constrained direct requirements to the tested lock.
- Strengthened Git/Docker exclusions and source/staged secret scanning; added seven release-tooling regression cases.
- Added static release checks and deterministic clean archive layout, source hashes, change inventory and external ZIP manifest/checksum.
- Re-ran local acceptance and final extracted-source acceptance; see docs/STATUS.md and the external manifest for measured evidence.
- Live PostgreSQL, connectors, notification canaries, target deployment, and hosted CI remain UNVERIFIED.

The earlier sections below are retained from the supplied release; no additional historical releases are invented.

## 0.28.0 — production isolation fixes

- Explicit development-only mock and fixture gates; fail-closed PostgreSQL/production configuration.
- Canonical Suricata occurrence IDs; idempotent multi-collector evidence merge.
- Tenant-scoped ORM reads/writes plus composite database constraints; isolated REAL/TEST incident correlation and inventory; replay blocked from live ingest.
- Dispatch-time channel/legacy/canary/tenant/test policy with SUPPRESSED reasons and versioned safe payloads.
- UTC from/to filtering and agent-scoped metrics; original sensor liveness and heartbeat API.
- Stable Case Pack JSON; immutable event sets, versioned deterministic replay results; neutral What Changed snapshot comparison.
- Incident summary, disposition, updated_at and optional terminal CLOSED state.
- Alembic 0003 with preserved IDs/data, historical-mode checks and snapshot immutability triggers.
- Non-root Docker/Compose, TLS/VPN proxy guidance, portable secret scan and real connector acceptance steps.
- Regenerated OpenAPI/contracts and added production, boundary, investigation, migration and HTTP-shape regression suites.
- Final tenant/mode merge FKs, all-model tenant/FK/index checks, unrelated-table migration preservation, and PostgreSQL constraint-name/index handling.
- Isolated acceptance scripts with measured JUnit category results, real Uvicorn smoke, guarded PostgreSQL round-trip/full-suite runner, runtime-generated test identities and explicit open live-integration gates.

## 0.27.0 — supplied baseline

Original Phase 24/26/27 backend, notification outbox, deployment templates and 60 baseline tests. Retained architecture and supported roles.
