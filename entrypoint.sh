#!/bin/sh

set -eu

APP_TYPE="${APP_TYPE:-api}"
PORT="${GUNIPORT:-9000}"
GUNICORN_APP="${GUNICORN_APP:-skel_v3.app:app_factory}"
WORKER_TARGET="${WORKER_TARGET:-skel_v3.app}"

if [ "$APP_TYPE" = "api" ]; then
    echo "Starting API with Gunicorn on port $PORT"
    if command -v poetry >/dev/null 2>&1; then
        exec poetry run gunicorn --factory -b "0.0.0.0:$PORT" "$GUNICORN_APP" --access-logfile=-
    fi
    exec gunicorn --factory -b "0.0.0.0:$PORT" "$GUNICORN_APP" --access-logfile=-
fi

if [ "$APP_TYPE" = "worker" ]; then
    echo "Starting worker module: $WORKER_TARGET"
    if command -v poetry >/dev/null 2>&1; then
        exec poetry run python -m "$WORKER_TARGET"
    fi
    exec python -m "$WORKER_TARGET"
fi

echo "Invalid APP_TYPE: $APP_TYPE. Use 'api' or 'worker'." >&2
exit 2
