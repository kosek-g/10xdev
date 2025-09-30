#!/bin/bash

# Azure Container/App Service startup script for Django
echo "Starting Finance Tracker application..."

# Exit on any error
set -e

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Wait for database to be ready
echo "Waiting for database connection..."
python manage.py check --database default

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Create superuser if it doesn't exist (optional for development)
# echo "Creating superuser..."
# python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'change-this-password')"

# Start Gunicorn server with production settings
echo "Starting Gunicorn server..."
exec gunicorn \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --worker-class sync \
    --worker-connections 1000 \
    --timeout 600 \
    --keepalive 5 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --preload \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    FinanceTracker.wsgi:application