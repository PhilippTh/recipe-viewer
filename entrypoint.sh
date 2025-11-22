#!/bin/sh
set -e

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
