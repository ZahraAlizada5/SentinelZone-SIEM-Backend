# Configuration reference

Settings are defined in `app/config.py`. Environment variables override `.env`; `.env` is loaded relative to the process working directory. Use the `SentinelZone-SIEM-Backend/` repository root as the working directory. Empty values fall back to defaults (`env_ignore_empty=True`). A deployment `.env` is private; `.env.example` contains only blank credentials and an intentionally unusable URL placeholder.

| Area | Variables and behavior |
|---|---|
| Application | `APP_ENV`: development/test/production; code defaults to development, supplied template to production. `DEBUG=false`. `DEFAULT_TENANT_ID=lab` is a generic tenant label; choose before initial migration. |
| Development gates | `ALLOW_FIXTURES=false`, `ENABLE_LEGACY_MOCK_ROUTES=false`. Fixtures require development/test opt-in; legacy mocks require development opt-in. Production rejects both flags. `FIXTURES_DIR` can override the bundled fixture directory for development. |
| Database | `DATABASE_URL` must be PostgreSQL/psycopg in production. Bare `postgresql://` is normalized. SQLite default is only for development. Compose's `POSTGRES_*` values initialize PostgreSQL; they are not backend Settings fields. |
| Auth | `AUTH_DB_ENABLED=true`; blank `AUTH_TOKENS` uses DB users only. Optional bootstrap format is `RANDOM_TOKEN:username:role:tenant`, semicolon-separated. Production tokens must be random and at least 32 characters. No actual tokens are supplied. |
| Browser/proxy | `CORS_ORIGINS` is comma-separated exact origins. `CORS_ALLOW_CREDENTIALS=true` forbids wildcard origins in production. `FORWARDED_ALLOW_IPS` is consumed by Uvicorn/Docker, not Pydantic Settings; trust only your proxy peer. |
| Splunk | `SPLUNK_URL` is the HTTPS management API base; `SPLUNK_TOKEN` is a read-only bearer credential; `SPLUNK_CA_FILE` optionally names a readable CA bundle; `SPLUNK_INDEX=main` is an example to replace. Search recognizes wazuh/suricata/cowrie sourcetype prefixes. |
| Wazuh | HTTPS `WAZUH_URL`, read-only `WAZUH_USERNAME`/`WAZUH_PASSWORD`, optional `WAZUH_CA_FILE`. `WAZUH_ALERTS_PATH=/alerts` is an adapter contract, not a claim about the standard Manager API. |
| CryptoGuard | HTTPS `CRYPTOGUARD_URL`, bearer `CRYPTOGUARD_READ_KEY`, optional `CRYPTOGUARD_CA_FILE`; `CRYPTOGUARD_EVENTS_PATH=/v1/telemetry` must match the upstream deployment. |
| Connector limits | `CONNECTOR_TIMEOUT_SECONDS=10`; `CONNECTOR_RETRIES=2` is the maximum request attempts in the common request helper. `MAX_INGEST_EVENTS=10000` bounds each connector batch. `INGEST_OVERLAP_SECONDS=120` re-reads recent events; dedup merges evidence. |
| Scheduling | Code defaults `INGEST_INTERVAL_SECONDS=0` / `DISPATCH_INTERVAL_SECONDS=0` disable background loops. The production template sets 30 / 5 seconds. Use zero when choosing external timers/CLI workers. |
| Correlation | `CORRELATION_WINDOW_MINUTES=15`, range 1..1440. Published Replay v1 uses 15, v2 uses 5; other live windows receive a versioned label. |
| Connector freshness | `STALE_AFTER_MINUTES=15` degrades stale successful polls; this is not proof of individual sensor liveness. |
| Sensor liveness | `SENSOR_EXPECTED_INTERVALS={}` maps sensors to positive seconds only after a real cadence is verified. `SENSOR_OFFLINE_MULTIPLIER=3` sets the offline threshold; unconfigured cadence remains unknown/not_configured. |
| Telegram | `TELEGRAM_ENABLED=false`, blank `TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID`. Enabled delivery requires both. |
| SMS | `SMS_ENABLED=false`, blank `SMS_WEBHOOK_URL`/`SMS_WEBHOOK_TOKEN`/`SMS_TO`. Provider receives JSON with `to` and `message`; production requires HTTPS. |
| Migration policy | `LEGACY_TELEGRAM_ACTIVE` suppresses new Telegram sends. `TELEGRAM_CANARY_ENABLED` restricts sends to comma-separated `TELEGRAM_CANARY_HOSTS`; it does not reconfigure the legacy sender. |
| Delivery policy | `NOTIFICATION_TENANT_ID` defaults to the configured tenant. `ALLOW_TEST_NOTIFICATIONS=false`; opt-in test delivery is Telegram-only and requires a separate `TEST_TELEGRAM_CHAT_ID`. `NOTIFY_MAX_ATTEMPTS=5`; `NOTIFICATION_TEMPLATE_VERSION=1`. |
| Action proposals | `PROTECTED_TARGETS` is a comma-separated host/IP list. `PROTECTED_ASSET_ROLES` defaults to infrastructure roles listed in the example. This release records proposals and decisions only; no action executor exists. |

URLs must not embed connector credentials. Mount private CA files read-only and use their in-container paths. Unconfigured connectors remain visible rather than supplying fixture data. CORS/proxy settings do not replace firewall/VPN restrictions. Restart all relevant processes after changing settings; queued notification policy is re-evaluated on dispatch using the newly loaded configuration.

A deployment has one connector/provider configuration tenant. Multi-tenant data access is isolated, but per-tenant secret stores and provider configurations are not implemented. See [integration](INTEGRATION.md) and [limitations](KNOWN_LIMITATIONS.md).
