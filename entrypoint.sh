#!/bin/sh

set -e

echo "Applying database migrations..."
# Applies all pending migrations
python manage.py migrate --noinput

echo "Collecting static files..."
# Collects all static files into STATIC_ROOT
python manage.py collectstatic --noinput

echo "Starting application..."
# Executes the given CMD from Dockerfile
exec "$@"
