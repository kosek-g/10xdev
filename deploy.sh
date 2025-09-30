#!/bin/bash

# Azure deployment script for Finance Tracker
set -e

echo "Starting deployment..."

# Install Python dependencies
if [ -f requirements.txt ]; then
    echo "Installing Python dependencies..."
    pip install -r requirements.txt
fi

# Set Django settings for Azure
export DJANGO_SETTINGS_MODULE=FinanceTracker.azure_settings

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Deployment completed successfully!"