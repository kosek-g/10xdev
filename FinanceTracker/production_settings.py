# Azure Production Settings
# This file contains additional settings for Azure deployment

import os
from .settings import *

# Production security settings
DEBUG = False
ALLOWED_HOSTS = [
    'financetracker.azurewebsites.net',
    'localhost', 
    '127.0.0.1',
    '.azurewebsites.net'
]

# Database configuration for Azure PostgreSQL
if 'AZURE_POSTGRESQL_HOST' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('AZURE_POSTGRESQL_NAME'),
            'USER': os.environ.get('AZURE_POSTGRESQL_USER'),
            'PASSWORD': os.environ.get('AZURE_POSTGRESQL_PASSWORD'),
            'HOST': os.environ.get('AZURE_POSTGRESQL_HOST'),
            'PORT': '5432',
            'OPTIONS': {
                'sslmode': 'require',
            }
        }
    }

# Static files configuration for Azure
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files configuration for Azure Blob Storage (optional)
if 'AZURE_STORAGE_ACCOUNT_NAME' in os.environ:
    DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
    AZURE_ACCOUNT_NAME = os.environ.get('AZURE_STORAGE_ACCOUNT_NAME')
    AZURE_ACCOUNT_KEY = os.environ.get('AZURE_STORAGE_ACCOUNT_KEY')
    AZURE_CONTAINER = 'media'

# Security settings for production
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}