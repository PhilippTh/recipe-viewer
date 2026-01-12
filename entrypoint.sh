#!/bin/sh
set -e

# Wait for PostgreSQL to be ready (if using PostgreSQL)
if [ -n "$POSTGRES_HOST" ]; then
    echo "Waiting for PostgreSQL at $POSTGRES_HOST:${POSTGRES_PORT:-5432}..."
    while ! python -c "import socket; s = socket.socket(); s.settimeout(1); s.connect(('$POSTGRES_HOST', ${POSTGRES_PORT:-5432})); s.close()" 2>/dev/null; do
        echo "PostgreSQL is unavailable - sleeping"
        sleep 1
    done
    echo "PostgreSQL is available"
fi

# Run migrations (skip with SKIP_MIGRATIONS=true)
if [ "${SKIP_MIGRATIONS:-false}" != "true" ]; then
    echo "Running database migrations..."
    python manage.py migrate --noinput
else
    echo "Skipping database migrations (SKIP_MIGRATIONS=true)"
fi

# Collect static files (skip with SKIP_COLLECTSTATIC=true)
if [ "${SKIP_COLLECTSTATIC:-false}" != "true" ]; then
    echo "Collecting static files..."
    python manage.py collectstatic --noinput --clear
else
    echo "Skipping static files collection (SKIP_COLLECTSTATIC=true)"
fi

echo "Starting Uvicorn server..."
exec uvicorn recipe_viewer.asgi:application \
    --host 0.0.0.0 \
    --port "${PORT:-8000}" \
    --workers "${WORKERS:-4}" \
    --log-level "${LOG_LEVEL:-info}"
