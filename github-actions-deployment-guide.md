# GitHub Actions CI/CD Deployment Guide

This guide walks you through deploying your Finance Tracker application using GitHub Actions with Docker to Azure Container Instances.

## 🚀 Quick Start

1. **Fork/Clone** this repository
2. **Set up Azure resources** (see [Azure Setup](#azure-setup))
3. **Configure GitHub secrets** (see [GitHub Secrets](#github-secrets))
4. **Push to main branch** to trigger deployment

## 📋 Prerequisites

- GitHub repository
- Azure subscription
- Azure CLI installed locally
- Docker (for local testing)

## 🏗️ Architecture Overview

```
GitHub → GitHub Actions → Azure Container Registry → Azure Container Instances
   ↓
Unit Tests → Security Scan → Build Docker → Deploy Staging → Deploy Production
```

### Pipeline Stages:

1. **Test Stage**: Runs 21 unit tests with PostgreSQL
2. **Security Scan**: Safety checks and Bandit security analysis
3. **Build & Push**: Multi-stage Docker build to Azure Container Registry
4. **Deploy Staging**: Deploy to staging environment for testing
5. **Deploy Production**: Blue-green deployment to production
6. **Notification**: Success/failure notifications

## 🔧 Azure Setup

### 1. Create Resource Group
```bash
az group create --name finance-tracker-rg --location eastus
```

### 2. Create Container Registry
```bash
az acr create \
  --resource-group finance-tracker-rg \
  --name financetracker \
  --sku Basic \
  --admin-enabled true
```

### 3. Create PostgreSQL Database
```bash
# Create PostgreSQL server
az postgres server create \
  --resource-group finance-tracker-rg \
  --name finance-tracker-db \
  --location eastus \
  --admin-user financeadmin \
  --admin-password "YourSecurePassword123!" \
  --sku-name B_Gen5_1

# Create database
az postgres db create \
  --resource-group finance-tracker-rg \
  --server-name finance-tracker-db \
  --name financetracker

# Configure firewall
az postgres server firewall-rule create \
  --resource-group finance-tracker-rg \
  --server finance-tracker-db \
  --name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0
```

### 4. Create Service Principal
```bash
az ad sp create-for-rbac \
  --name "finance-tracker-github-actions" \
  --role contributor \
  --scopes /subscriptions/YOUR_SUBSCRIPTION_ID \
  --sdk-auth
```

## 🔐 GitHub Secrets

Add these secrets in your GitHub repository (`Settings > Secrets and variables > Actions`):

### Required Secrets:
```
AZURE_CREDENTIALS              # Service principal JSON from step 4 above
AZURE_CONTAINER_REGISTRY_NAME  # financetracker
AZURE_CONTAINER_REGISTRY_USERNAME  # From: az acr credential show --name financetracker
AZURE_CONTAINER_REGISTRY_PASSWORD  # From: az acr credential show --name financetracker
AZURE_RESOURCE_GROUP           # finance-tracker-rg
AZURE_CONTAINER_GROUP          # finance-tracker-container
DJANGO_SECRET_KEY              # Generate secure random key
AZURE_POSTGRESQL_HOST          # finance-tracker-db.postgres.database.azure.com
AZURE_POSTGRESQL_NAME          # financetracker
AZURE_POSTGRESQL_USER          # financeadmin@finance-tracker-db
AZURE_POSTGRESQL_PASSWORD      # YourSecurePassword123!
```

📖 **Detailed setup instructions**: See `github-secrets-setup.md`

## 🌐 GitHub Environments

Create two environments in your repository:

1. **staging** - Automatic deployment from main branch
2. **production** - Manual approval required (recommended)

Setup: `Settings > Environments > New environment`

## 🔄 Workflow Features

### ✅ Continuous Integration
- **Automated testing** with PostgreSQL test database
- **Code coverage** reporting with Codecov
- **Security scanning** with Safety and Bandit
- **Django checks** for configuration issues

### 🐳 Docker Build
- **Multi-stage build** for optimized image size
- **Security scanning** with Trivy
- **Automatic tagging** with branch name and SHA
- **Layer caching** for faster builds

### 🚀 Deployment Strategy
- **Blue-green deployment** with zero downtime
- **Staging environment** for validation
- **Health checks** and smoke tests
- **Automatic rollback** on failure
- **Environment cleanup** after successful deployment

### 📊 Monitoring & Notifications
- **Deployment status** notifications
- **Container health checks** with curl
- **Resource utilization** monitoring
- **Log aggregation** with Azure Monitor

## 🎯 Deployment URLs

After successful deployment:

- **Staging**: `http://finance-tracker-staging-{run-number}.eastus.azurecontainer.io:8000`
- **Production**: `http://finance-tracker-prod.eastus.azurecontainer.io:8000`

## 📱 Local Development

### Run with Docker Compose
```bash
# Copy environment template
cp .env.azure.template .env.local

# Edit .env.local with your values
nano .env.local

# Start services
docker-compose -f docker-compose.azure.yml up -d

# View logs
docker-compose -f docker-compose.azure.yml logs -f
```

### Run Tests Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 🛠️ Workflow Customization

### Environment Variables
Edit `.github/workflows/ci-cd.yml` to customize:

```yaml
env:
  AZURE_LOCATION: eastus  # Change Azure region
  IMAGE_NAME: finance-tracker  # Change image name
```

### Resource Allocation
Adjust container resources:

```yaml
--cpu 2 \      # CPU cores
--memory 4     # Memory in GB
```

### Test Configuration
Modify test database settings:

```yaml
services:
  postgres:
    env:
      POSTGRES_DB: test_financetracker  # Test database name
```

## 🔍 Monitoring & Troubleshooting

### View Deployment Logs
```bash
# GitHub Actions logs
# Go to Actions tab in your repository

# Azure Container logs
az container logs \
  --resource-group finance-tracker-rg \
  --name finance-tracker-container

# Stream logs
az container logs \
  --resource-group finance-tracker-rg \
  --name finance-tracker-container \
  --follow
```

### Health Checks
The application includes a health check endpoint:
```
GET /health/
```

Returns:
- `200 OK` - Application healthy
- `500 Error` - Application issues

### Common Issues

1. **Build Failures**
   - Check Docker syntax
   - Verify requirements.txt

2. **Test Failures**
   - Check database connectivity
   - Review test logs in Actions

3. **Deployment Failures**
   - Verify Azure credentials
   - Check resource quotas
   - Review container logs

4. **Database Connection Issues**
   - Verify PostgreSQL server status
   - Check firewall rules
   - Validate connection strings

## 🔒 Security Features

### Container Security
- **Non-root user** execution
- **Minimal base image** (Python slim)
- **Security scanning** with Trivy
- **Vulnerability reporting** to GitHub Security

### Network Security
- **HTTPS enforcement** with Nginx
- **Security headers** configuration
- **Firewall rules** for database access
- **Private container registry**

### Secret Management
- **GitHub Secrets** for sensitive data
- **Environment-based** configuration
- **No secrets in code** or images
- **Azure Key Vault** integration ready

## 📈 Performance Optimization

### Docker Optimizations
- **Multi-stage builds** reduce image size
- **Layer caching** speeds up builds
- **Minimal dependencies** in runtime image
- **Health checks** for reliability

### Application Performance
- **Gunicorn** WSGI server
- **Static file serving** with WhiteNoise
- **Database connection pooling**
- **Nginx reverse proxy** (optional)

## 🚦 Next Steps

1. **Custom Domain**: Configure custom domain with SSL
2. **CDN**: Add Azure CDN for static files
3. **Monitoring**: Set up Application Insights
4. **Scaling**: Configure auto-scaling rules
5. **Backup**: Implement database backup strategy
6. **Security**: Integrate Azure Security Center

## 📚 Additional Resources

- [Azure Container Instances Documentation](https://docs.microsoft.com/en-us/azure/container-instances/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Django Deployment Best Practices](https://docs.djangoproject.com/en/stable/howto/deployment/)
- [Docker Multi-stage Builds](https://docs.docker.com/develop/dev-best-practices/dockerfile_best-practices/)

## 🆘 Support

For issues:
1. Check GitHub Actions logs
2. Review Azure Container Instance logs
3. Verify GitHub secrets configuration
4. Consult troubleshooting section above

---

🎉 **Congratulations!** Your Finance Tracker application is now ready for professional deployment with GitHub Actions and Azure!