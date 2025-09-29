#!/bin/bash

# Azure App Service startup script for Django
echo "Starting Finance Tracker application..."

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Create superuser if it doesn't exist (optional)
# echo "Creating superuser..."
# python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'change-this-password')"

# Start Gunicorn server
echo "Starting Gunicorn server..."
exec gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout 600 FinanceTracker.wsgi:application