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

# Compile translation messages (skip with SKIP_COMPILEMESSAGES=true)
if [ "${SKIP_COMPILEMESSAGES:-false}" != "true" ]; then
    echo "Compiling translation messages..."
    python manage.py compilemessages
else
    echo "Skipping translation compilation (SKIP_COMPILEMESSAGES=true)"
fi

# Create superuser if it doesn't exist (always runs, fast idempotent check)
echo "Creating superuser if needed..."
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print('Superuser created: username=admin, password=admin')
else:
    print('Superuser already exists')
" || echo "Superuser creation skipped"

echo "Starting Uvicorn server..."
exec uvicorn recipe_viewer.asgi:application \
    --host 0.0.0.0 \
    --port "${PORT:-8000}" \
    --log-level "${LOG_LEVEL:-info}"
