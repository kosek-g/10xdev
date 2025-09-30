#!/bin/bash

# Azure Container/App Service startup script for Django
echo "Starting Finance Tracker application..."

# Exit on any error
set -e

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Wait for database to be ready with retries
echo "Waiting for database connection..."
for i in {1..30}; do
    echo "Database connection attempt $i..."
    if python manage.py check --database default; then
        echo "Database is ready!"
        break
    else
        echo "Database not ready, waiting 5 seconds..."
        sleep 5
    fi
    if [ $i -eq 30 ]; then
        echo "Database connection failed after 30 attempts"
        exit 1
    fi
done

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