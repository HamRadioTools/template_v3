# Template v3

Skeleton template for Python >=3.12 services with dual runtime support:
- API mode (`APP_TYPE=api`)
- Worker mode (`APP_TYPE=worker`)

The template is spec-driven: implementation should follow `openspec/`.

## Features

- API + worker runtime in one package.
- Worker supports two modes:
  - `WORKER_MODE=oneshot` (default): run once and exit.
  - `WORKER_MODE=loop`: poll continuously with graceful signal shutdown.
- Unified container entrypoint with explicit `APP_TYPE` routing.
- Multi-stage Docker build for smaller runtime image.
- Structured JSON logging to stdout.
- Postgres + Redis wiring and pytest scaffold.

## Project Layout

- `src/skel_v3/` — app package
  - `api/` — Flask routes and health checks
  - `worker/` — worker runtime helpers
  - `logs/`, `db/`, `util/` — shared runtime components
- `openspec/` — source of truth for behavior/specifications
- `entrypoint.sh` — starts API (Gunicorn) or worker (`python -m`)
- `iac/docker/alpine.dockerfile` — multi-stage container build

## Configuration

### Runtime variables (`src/skel_v3/config.py`)

Execution and worker:
- `APP_TYPE` (default: `api`): `api` or `worker`
- `WORKER_MODE` (default: `oneshot`): `oneshot` or `loop`
- `WORKER_POLL_INTERVAL` (default: `5`): loop sleep interval in seconds

Service metadata:
- `SERVICE_NAME` (default: `skel-service`)
- `SERVICE_VERSION` (default: `0.1.0`)
- `SERVICE_NAMESPACE` (default: `default`)
- `SERVICE_ENV` (default: `local`)

Logging:
- `LOG_LEVEL` (default: `DEBUG` in `local/dev`, `INFO` otherwise)

Postgres:
- `PG_ENABLED` (default: `false`)
- `PG_HOST` (default: `postgres`)
- `PG_PORT` (default: `5432`)
- `PG_USER` (default: `postgres`)
- `PG_PASSWORD` (default: `postgres`)
- `PG_DBNAME` (default: `postgres`)
- `PG_MIN_CONN` (default: `1`)
- `PG_MAX_CONN` (default: `5`)
- `PG_SSLMODE` is currently not active in code (left as commented placeholder in `.env`)

Redis:
- `REDIS_ENABLED` (default: `false`)
- `REDIS_HOST` (default: `redis`)
- `REDIS_PORT` (default: `6379`)
- `REDIS_DB` (default: `0`)
- `REDIS_PASSWORD` (default: empty/`None`)
- `REDIS_MAX_CONN` (default: `20`)

### Entrypoint/container variables (`entrypoint.sh`)

API:
- `GUNIPORT` (default: `9000`)
- `GUNICORN_APP` (default: `skel_v3.app:app_factory`)

Worker:
- `WORKER_TARGET` (default: `skel_v3.app`)

## Runtime Behavior

`APP_TYPE=api`:
- `entrypoint.sh` runs Gunicorn with `--factory` and `GUNICORN_APP`.

`APP_TYPE=worker`:
- `entrypoint.sh` runs `python -m $WORKER_TARGET`.
- `skel_v3.app.main()` routes to `run_worker_app(config)`.
- `run_worker_app` uses `WORKER_MODE`:
  - `oneshot`: one work cycle then clean exit.
  - `loop`: repeated work until SIGINT/SIGTERM.

## OpenSpec Workflow

Read before coding:
1. `openspec/project.md`
2. relevant domain file under `openspec/specs/<domain>/spec.md`

Rules:
- spec is source of truth
- do not guess behavior not described in spec
- propose spec deltas when behavior changes are needed

## Quickstart

Install:
```bash
poetry install
```

Run API:
```bash
export APP_TYPE=api
poetry run python -m skel_v3.app
```

Run worker one-shot:
```bash
export APP_TYPE=worker WORKER_MODE=oneshot
poetry run python -m skel_v3.app
```

Run worker loop:
```bash
export APP_TYPE=worker WORKER_MODE=loop WORKER_POLL_INTERVAL=5
poetry run python -m skel_v3.app
```

Tests:
```bash
poetry run pytest
```
