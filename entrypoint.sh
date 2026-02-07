#!/bin/sh

# Default values for environment variables
DEFAULT_PORT=9000
PORT=${GUNIPORT:-$DEFAULT_PORT}

echo "Starting Gunicorn on port $PORT"

# First try Poetry-installed Gunicorn
if command -v poetry > /dev/null; then
    exec poetry run gunicorn -b 0.0.0.0:$PORT app:app --access-logfile=-
else
    # Fallback to globally installed Gunicorn
    exec gunicorn -b 0.0.0.0:$PORT app:app --access-logfile=-
fi
