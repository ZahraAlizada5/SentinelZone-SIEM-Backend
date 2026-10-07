# Integration guide

This standalone repository contains the SIEM Backend component of the SentinelZone SOC Platform. The separate [SentinelZone-SOC-Platform integration repository](https://github.com/Ulvu11/SentinelZone-SOC-Platform) coordinates the wider project. It does not replace the frontend, provision sensors, or require the original author's machine.

## Frontend

Configure the frontend's API base URL to the backend's trusted HTTPS reverse-proxy address (loopback `http://127.0.0.1:8003` for local development). Match the frontend origin in `CORS_ORIGINS`; keep privileged upstream credentials entirely on the backend. Send the user's backend bearer token in the Authorization header.

Use the [OpenAPI contract](openapi.json), [endpoint inventory](API_ENDPOINTS.md), and [API semantics](../API.md). Match existing response envelopes instead of expecting demo `/api/*` shapes. Present `data_complete=false`, degraded sources, unknown liveness, and TEST execution modes clearly; zero alerts does not mean all clear. Use the incident version/ETag in `If-Match` and handle 409 conflicts by reloading.

There is no automatic frontend code generation or dashboard migration in this package. Browser authentication storage, user experience, and end-to-end response mapping require frontend acceptance.

## Security sources

| Source | Path into this service | Required contract checks |
|---|---|---|
| Splunk | HTTPS read-only search export; normalizes allowlisted original sensor payloads | Index/sourcetype access, `_raw` JSON, UTC windows, truncation/errors, native IDs and evidence provenance |
| Wazuh | Manager-style authentication/health plus configurable alerts adapter | Standard Manager health is insufficient: confirm an actual alert provider and list/items/affected_items pagination contract |
| CryptoGuard | HTTPS health and configurable telemetry endpoint | Bearer read key, `event_id`, `observed_at`, risk/host identity, list/items and advancing cursor contract |
| Cowrie | Cowrie JSON collected by Splunk | Preserve event ID/session/timestamp/sensor fields; captured credentials are not copied into normalized metadata |
| Suricata | EVE JSON collected by Splunk | Preserve sensor identity, timestamp precision, flow/signature/traffic context; separate occurrences must remain distinct |

No direct Cowrie/Suricata listener is exposed. No `/v1/cryptoguard/...` route is provided by this backend. Windows sensor liveness requires a real heartbeat/telemetry adapter; a configuration entry does not install one.

1. Deploy/migrate with external delivery disabled.
2. Configure read-only endpoints/credentials and trusted CA paths privately.
3. Run `python scripts/connector-acceptance.py` and then `python scripts/connector-acceptance.py --fetch --minutes 15`. These are read-only upstream probes; they do not ingest or notify.
4. Follow [REAL_CONNECTOR_ACCEPTANCE.md](../REAL_CONNECTOR_ACCEPTANCE.md) for controlled ingestion, source-side count comparisons, duplicate evidence checks, and liveness validation.
5. Validate frontend mapping and only then perform deliberately enabled Telegram/SMS canaries.

## Boundaries and extension points

Connectors return `RawEvent`; normalizers produce `NormalizedEvent`. Keep `original_sensor` distinct from `collector_path`, and `agent_ip` distinct from `src_ip`. Tenant ownership is established by trusted configuration/identity, not incoming untrusted tenant fields. Replay does not call ingestion, delivery, or proposal execution.

The built-in connectors and notification recipients belong to one configured tenant. Additional tenants need separately configured workers/deployments or a reviewed per-tenant configuration store. Add focused mock contract tests before modifying a connector, then obtain live acceptance evidence from the actual provider. Do not label mocked HTTP as live acceptance.

Notification integration supports Telegram and a generic SMS webhook. Retries are bounded; a crash between provider send and DB commit can duplicate delivery. Action approval remains a skeleton; Phase 28 AI / Phase 29 executor integration must be implemented as a separate reviewed change.
