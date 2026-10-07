# From ZIP to a running backend

Release 0.28.1. Start in the extracted `SentinelZone-SIEM-Backend/` directory. You need Docker with Compose v2, or CPython 3.12 plus PostgreSQL for native production. Keep the supplied `.env.example`; your real `.env` stays private.

## Docker Compose

1. Copy `.env.example` to `.env` (`cp .env.example .env` on Linux/macOS; `Copy-Item .env.example .env` in PowerShell).
2. Generate a unique password with your password manager. Put it in `POSTGRES_PASSWORD` and in `DATABASE_URL`; use hostname `postgres` for Compose. URL-encode non-URL-safe password characters. An optional local generator is `python -c "import secrets; print(secrets.token_hex(32))"`.
3. Keep production mode, fixture/mock flags false, and notification flags false. Set the frontend's exact origin in `CORS_ORIGINS`. Leave connectors empty until their real contracts are configured.
4. Run:

```bash
docker compose config --quiet
docker compose up -d --build
docker compose ps
docker compose exec backend alembic current
docker compose exec backend alembic check
docker compose exec backend python -m app.cli create-user soc-admin admin
curl --fail-with-body http://127.0.0.1:8003/health
```

In PowerShell, use `curl.exe` or `Invoke-RestMethod http://127.0.0.1:8003/health`. Migration happens automatically before Uvicorn starts. Store the generated admin token securely; do not rerun create-user for the same name. Protected endpoints are denied until an identity exists.

`database=healthy` with `status=degraded` and `not_configured` connectors is expected before integration. Visit `http://127.0.0.1:8003/docs` for route documentation. The bearer token is supplied as the Authorization header; the contract does not define an OAuth login flow.

Stop with `docker compose down`. Do **not** add `-v` unless you deliberately intend to delete the database volume. Changing `POSTGRES_PASSWORD` in `.env` does not rotate an already initialized PostgreSQL role: follow PostgreSQL administration procedures and update both settings consistently.

## Native Python

See [INSTALL.md](../INSTALL.md) for Linux, PowerShell, and isolated SQLite development. Run tests in a separate clean checkout with no deployment `.env`:

```bash
python -m pip install -r requirements.lock.txt
python scripts/acceptance.py
```

The POSIX loopback acceptance runner uses inherited file descriptors. Run full acceptance in Linux, WSL2, or CI. Native Windows runtime has not been tested here.

## Verify a protected read without printing a token

With dependencies installed and the server running, this prompts securely:

```bash
python -c "import getpass,httpx; token=getpass.getpass('Backend token: '); r=httpx.get('http://127.0.0.1:8003/v1/alerts',headers={'Authorization':'Bearer '+token}); r.raise_for_status(); print('Authenticated alerts request:',r.status_code)"
```

## Troubleshooting

| Symptom | Check |
|---|---|
| Compose reports an unset password/URL | Edit both database values in `.env`; inspect with `config --quiet`, which does not print secrets |
| Backend fails before listening | Placeholder/config validation, PostgreSQL readiness, migration output, database permissions |
| `/health` is degraded | Inspect connector states; missing integrations are not healthy telemetry |
| 401 / 403 | Correct bearer token, enabled user, and required role |
| Browser CORS error | Exact frontend scheme/host/port in `CORS_ORIGINS`; restart |
| Empty alerts after fixture ingest | Fixtures are TEST; explicitly request `include_test=true` and TEST incidents |
| Acceptance refuses `.env` | Use a fresh source copy; do not test against deployment secrets/data |

Review startup logs locally and redact before sharing. Do not disable TLS or production guards to make a failing integration appear healthy. Target-host Docker acceptance remains [UNVERIFIED](STATUS.md).
