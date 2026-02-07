# Template v3

Skeleton template for a Python >=3.12 microservice (API + worker) with ready-to-wire observability and infra hooks. This template is ready for Rust integration with PyO3.

## Features

- API + worker entrypoint controlled by `APP_TYPE` (`api`/`worker`).
- Container-friendly `entrypoint.sh` that runs Gunicorn for API or a Python module for worker; env-driven.
- Health/ready endpoints with optional Redis-backed API-key protection.
- Structured JSON logging, Postgres + Redis wiring, pytest scaffolding.
- Name/version alignment helper (`set_versname.py`) to keep code, env files, and folders consistent.

## Project Layout

- `src/skel_v3/` — app package.
  - `api/` — Flask bootstrap, routes, health checks.
  - `worker/` — worker loop placeholder.
  - `.env` — service-level defaults (used by `dotenv` on local).
- `.env` — outer file for local tooling (e.g., `PYTHONPATH="src/<pkg>"`).
- `entrypoint.sh` — container entrypoint; reads `APP_TYPE`, `APP_MODULE`, `GUNICORN_APP`, `WORKER_TARGET`.
- `pyproject.toml` — source of truth for project `name` and `version`.
- `set_versname.py` — synchronizes names/versions across code and env files.

## Configuration

| Variable              | Description                                         |
|-----------------------|-----------------------------------------------------|
| `APP_TYPE`            | `api` (default) or `worker`.                        |
| `SERVICE_ENV`         | Environment name (`local`, `dev`, `prod`, ...).     |
| `SERVICE_NAME`        | Logical service identifier shown in logs.           |
| `LOG_LEVEL`           | `DEBUG`, `INFO`, ... (auto defaults per env).       |
| `PG_*`                | Postgres connection + pool sizing.                  |
| `REDIS_*`             | Redis connection settings for API key checks.       |

### Configuration Flow

- Local: `.env` (outer) sets `PYTHONPATH="src/<package>"`; `src/<package>/.env` sets service defaults.
- Runtime config: `src/skelv2/config.py` loads from environment (12-factor). Use env vars in containers/CI.
- Startup:
  - `APP_TYPE=api` → Gunicorn runs `<APP_MODULE>.wsgi:app`.
  - `APP_TYPE=worker` → `python -m <WORKER_TARGET>`.
  - Defaults: `APP_MODULE=<project_name>`, `GUNICORN_APP=<project_name>.wsgi:app`, `WORKER_TARGET=<project_name>.app`.

## Quickstart

Install dependencies:

```bash
pip install poetry==1.8.3
poetry install
```

Run API:

```bash
export APP_TYPE=api FLASK_PORT=9000
poetry run python -m skelv2.app
```

Run worker:

```bash
export APP_TYPE=worker
poetry run python -m skelv2.app
```

## Docker

Build:

```bash
docker build -f iac/docker/alpine.dockerfile -t skel_v3 .
```

Key env vars:

- `APP_TYPE`: `api` or `worker`
- `GUNIPORT`: Gunicorn port (default 9000)
- `APP_MODULE` / `GUNICORN_APP` / `WORKER_TARGET`: override module names if renamed
- `REDIS_*`, `PG_*`: backing services

`entrypoint.sh` chooses the command based on `APP_TYPE` and module vars.

## HTTP Endpoints

### `GET /health`

Simple JSON liveness probe:

```json
{
  "status": "ok",
  "service": "micro-service",
  "version": "0.1.0"
}
```

### `GET /ready`

Lightweight readiness probe. Extend it if you need deeper datastore checks.

## Logging

Structured JSON to stdout (API and worker). Fields include service, env, file, line, request_id (API), etc., ready for log collectors (Loki/SIEM).

- Werkzeug/Gunicorn access logs remain enabled so HTTP traffic is also emitted as JSON; use `LOG_LEVEL` for noise control and override with `FLASK_DEBUG` when you still want the Flask debugger/reloader locally.

## Testing

```bash
poetry run pytest
```

The default test disables Postgres and Redis so it runs without external
services.

## Future work

1. Extend easily with new routes/worker tasks.
1. Add new tests as new features are added.
