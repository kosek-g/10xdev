# Multi-stage build for production optimization
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies for building
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /tmp/
RUN pip install --upgrade pip \
    && pip install --user --no-cache-dir -r /tmp/requirements.txt

# Production stage
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH=/home/appuser/.local/bin:$PATH

# Install runtime dependencies only
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser

# Copy Python dependencies from builder stage
COPY --from=builder /root/.local /home/appuser/.local

# Set work directory
WORKDIR /app

# Copy project files
COPY --chown=appuser:appuser . /app/

# Switch to non-root user
USER appuser

# Create necessary directories
RUN mkdir -p /app/staticfiles /app/mediafiles

# Set Django settings for production
ENV DJANGO_SETTINGS_MODULE=FinanceTracker.azure_settings

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Expose port
EXPOSE 8000

# Copy and use startup script
COPY --chown=appuser:appuser startup.sh /app/startup.sh
RUN chmod +x /app/startup.sh

# Run the application using Gunicorn
CMD ["/app/startup.sh"]