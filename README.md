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

Core:
- `APP_TYPE`: `api` (default) or `worker`
- `SERVICE_ENV`: environment name (`local`, `dev`, `prod`, ...)
- `SERVICE_NAME`: service identifier in logs
- `SERVICE_VERSION`: service version metadata
- `LOG_LEVEL`: root log level

Worker:
- `WORKER_MODE`: `oneshot` (default) or `loop`
- `WORKER_POLL_INTERVAL`: interval in seconds for loop mode (default `5`)

API container:
- `GUNIPORT`: Gunicorn bind port (default `9000`)
- `GUNICORN_APP`: factory target (default `skel_v3.app:app_factory`)

Worker container:
- `WORKER_TARGET`: python module target (default `skel_v3.app`)

Datastores:
- `PG_*`: PostgreSQL connectivity/pool
- `REDIS_*`: Redis connectivity/pool

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
