# Native Python installation

Use CPython **3.12**. Linux/Python 3.12.14 is the measured runtime. PostgreSQL is required in production; Compose targets PostgreSQL 16. Provision an application role/database through your normal administrator process. The production role must not be a superuser; use a separately managed migration role if your deployment separates DDL and runtime permissions.

## Linux / macOS shell

From the `SentinelZone-SIEM-Backend/` repository root, before creating a deployment `.env`:

```bash
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.lock.txt
python -m pip check
python scripts/acceptance.py
cp .env.example .env
chmod 600 .env
```

Set your PostgreSQL URL, exact frontend origin, and chosen tenant in `.env`. Replace the password placeholder. Native `DATABASE_URL` uses your database hostname; `postgres` is the Compose service name, not a universal hostname. Empty connector URLs are allowed and reported as not configured. Keep fixture/mock flags and external notification delivery disabled.

```bash
python -c 'from app.config import get_settings; get_settings().validate_runtime(); print("configuration accepted")'
alembic upgrade head
alembic check
python -m app.cli create-user soc-admin admin
uvicorn app.main:app --host 127.0.0.1 --port 8003
```

Create-user shows a new token once and stores only its hash. Test `/health` from another terminal. Use a TLS reverse proxy before remote access; see [DEPLOYMENT.md](DEPLOYMENT.md).

## PowerShell

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.lock.txt
python -m pip check
Copy-Item .env.example .env
```

Edit `.env` privately, then run the same Alembic, create-user, and Uvicorn commands. If activation is restricted, invoke `.venv\Scripts\python.exe` directly; do not weaken machine-wide execution policies. Restrict `.env` through Windows file permissions. The uvloop pin is platform-conditioned and colorama is pinned for Windows, but native Windows installation/runtime is **UNVERIFIED**. Full acceptance uses a POSIX socket-FD smoke harness; use WSL2/Linux/CI for that command.

## Isolated SQLite development, without real integrations

Install dependencies first. In a separate development copy, copy `.env.example` to `.env` and change:

```dotenv
APP_ENV=development
DATABASE_URL=sqlite:///./sentinelzone-dev.db
ALLOW_FIXTURES=false
INGEST_INTERVAL_SECONDS=0
DISPATCH_INTERVAL_SECONDS=0
```

Leave connector URLs and delivery credentials empty; keep mock/notification flags false. Migrate, create a user, and start Uvicorn as above. To exercise the supplied synthetic fixtures, explicitly set `ALLOW_FIXTURES=true` and run `python -m app.cli ingest`; those events are TEST/degraded and do not populate REAL inventory. This database is disposable development data, never production evidence. Do not commit it or run acceptance in this configured copy.

## Dependencies

`requirements.lock.txt` is the tested installation set. `requirements.txt` lists direct requirements constrained by that lock. Use a fresh environment when updating either; see [CONTRIBUTING.md](CONTRIBUTING.md). No dependencies, venv, certificates, or database binaries are included in the source ZIP.
