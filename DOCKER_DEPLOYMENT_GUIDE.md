# Ultimate Docker Deployment Guide for Finance Tracker

## 🚀 Complete Azure Container Deployment with CI/CD

This guide provides everything needed to deploy your Finance Tracker Django application using Docker containers on Azure with automated CI/CD pipelines.

## 📋 Prerequisites

- Azure subscription
- Azure CLI installed locally
- GitHub repository with the Finance Tracker code
- Docker installed locally (for testing)

## 🏗️ Step 1: Create Azure Resources

### 1.1 Login and Setup
```bash
# Login to Azure
az login

# Set your subscription (replace with your subscription ID)91.90.182.218
az account set --subscription "fa0b8e00-271b-498d-8c48-975518312f0e"

# Create resource group
az group create \
  --name finance-tracker-rg \
  --location "North Europe"
```

### 1.2 Create Azure Container Registry (ACR)
```bash
# Create container registry (must be globally unique)
az acr create \
  --resource-group finance-tracker-rg \
  --name financetracker10xdev \
  --sku Basic \
  --location "North Europe" \
  --admin-enabled true

# Get ACR credentials for GitHub secrets
az acr credential show \
  --name financetracker10xdev \
  --resource-group finance-tracker-rg
```

### 1.3 Create PostgreSQL Database (Ultra-Cheap Configuration)
```bash
# Create PostgreSQL Flexible Server (CHEAPEST option - B1ms)
az postgres flexible-server create \
  --resource-group finance-tracker-rg \
  --name 10xdev-finance-tracker-db \
  --location "North Europe" \
  --admin-user financeadmin \
  --admin-password "YourSecurePassword123!" \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --storage-size 32 \
  --version 15 \
  --backup-retention 7 \
  --high-availability Disabled \
  --zone 1

# Create database
az postgres flexible-server db create \
  --resource-group finance-tracker-rg \
  --server-name 10xdev-finance-tracker-db \
  --database-name financetracker

# Configure firewall to allow Azure services
az postgres flexible-server firewall-rule create \
  --resource-group finance-tracker-rg \
  --name 10xdev-finance-tracker-db \
  --rule-name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0

# Allow your local IP for management (replace with your actual IP)
# Get your IP: curl ifconfig.me
az postgres flexible-server firewall-rule create \
  --resource-group finance-tracker-rg \
  --name 10xdev-finance-tracker-db \
  --rule-name AllowMyIP \
  --start-ip-address 91.90.182.218 \
  --end-ip-address 91.90.182.218
```

### 1.4 Create Service Principal for GitHub Actions
```bash
# Create service principal for CI/CD
az ad sp create-for-rbac \
  --name "finance-tracker-github-actions" \
  --role contributor \
  --scopes /subscriptions/fa0b8e00-271b-498d-8c48-975518312f0e \
  --sdk-auth
```

**📝 IMPORTANT:** Save the entire JSON output - you'll need it for GitHub secrets!

## 🔐 Step 2: Configure GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions → New repository secret

Add these secrets:

### 2.1 Azure Authentication Secrets
```
AZURE_CREDENTIALS
```
**Value:** The complete JSON output from the service principal creation command above

### 2.2 Container Registry Secrets
```
AZURE_CONTAINER_REGISTRY_NAME
```
**Value:** `financetracker10xdev`

```
AZURE_CONTAINER_REGISTRY_USERNAME
```
**Value:** From `az acr credential show` command (usually same as registry name)

```
AZURE_CONTAINER_REGISTRY_PASSWORD
```
**Value:** Password from `az acr credential show` command

### 2.3 Azure Resource Configuration
```
AZURE_RESOURCE_GROUP
```
**Value:** `finance-tracker-rg`

```
AZURE_CONTAINER_GROUP
```
**Value:** `finance-tracker-container`

### 2.4 Django Application Secrets
```
DJANGO_SECRET_KEY
```
**Value:** Generate a secure secret key:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2.5 Database Connection Secrets
```
AZURE_POSTGRESQL_HOST
```
**Value:** `10xdev-finance-tracker-db.postgres.database.azure.com`

```
AZURE_POSTGRESQL_NAME
```
**Value:** `financetracker`

```
AZURE_POSTGRESQL_USER
```
**Value:** `financeadmin`

```
AZURE_POSTGRESQL_PASSWORD
```
**Value:** `YourSecurePassword123!` (the password you set during DB creation)

## 🚀 Step 3: Deploy Application

### 3.1 Push Code to Main Branch
```bash
# Ensure you're on the main branch
git checkout main

# Push your changes
git add .
git commit -m "Ready for Docker deployment"
git push origin main
```

### 3.2 Monitor Deployment
1. Go to your GitHub repository
2. Click on "Actions" tab
3. Watch the CI/CD pipeline execute
4. The pipeline will:
   - Run tests
   - Build and push Docker image to ACR
   - Deploy to staging environment
   - Run smoke tests
   - Deploy to production
   - Run health checks

### 3.3 Access Your Application
Once deployment completes:
- **Production URL:** `http://finance-tracker-prod.eastus.azurecontainer.io:8000`
- **Admin URL:** `http://finance-tracker-prod.eastus.azurecontainer.io:8000/admin/`

## 🛠️ Step 4: Post-Deployment Setup

### 4.1 Create Django Superuser
```bash
# Connect to the running container
az container exec \
  --resource-group finance-tracker-rg \
  --name finance-tracker-container \
  --exec-command "/bin/bash"

# Inside the container, create superuser
python manage.py createsuperuser

# Exit the container
exit
```

### 4.2 Test Your Application
1. Visit the production URL
2. Test user registration and login
3. Create some transactions
4. Access admin interface
5. Verify database connectivity

## 📊 Cost Optimization Tips

### Current Monthly Costs (Estimated):
- **PostgreSQL B1ms:** ~$12-17/month (or FREE with Azure credits)
- **Container Registry Basic:** ~$5/month
- **Container Instances:** ~$10-15/month (1 CPU, 2GB RAM)
- **Total:** ~$27-37/month

### Money-Saving Strategies:
```bash
# Stop database during development (saves ~$12-17/month)
az postgres flexible-server stop \
  --resource-group finance-tracker-rg \
  --name 10xdev-finance-tracker-db

# Start database when needed
az postgres flexible-server start \
  --resource-group finance-tracker-rg \
  --name 10xdev-finance-tracker-db

# Scale down container instances during off-hours
az container create \
  --resource-group finance-tracker-rg \
  --name finance-tracker-container-small \
  --cpu 0.5 \
  --memory 1
```

## 🔧 Manual Deployment Commands (if needed)

### Build and Test Locally
```bash
# Build Docker image locally
docker build -t finance-tracker .

# Test locally
docker run -d \
  --name finance-tracker-local \
  -p 8000:8000 \
  -e SECRET_KEY="your-test-secret-key" \
  -e DEBUG=True \
  finance-tracker

# Test the application
curl http://localhost:8000/

# Clean up
docker stop finance-tracker-local
docker rm finance-tracker-local
```

### Manual Azure Deployment
```bash
# Build and push to ACR
az acr build \
  --registry financetracker10xdev \
  --image finance-tracker:latest \
  .

# Deploy to Container Instances
az container create \
  --resource-group finance-tracker-rg \
  --name finance-tracker-container \
  --image financetracker10xdev.azurecr.io/finance-tracker:latest \
  --location "North Europe" \
  --dns-name-label finance-tracker-manual \
  --ports 8000 \
  --cpu 1 \
  --memory 2 \
  --environment-variables \
    DJANGO_SETTINGS_MODULE=FinanceTracker.azure_settings \
    SECRET_KEY="your-django-secret-key" \
    DEBUG=False \
    WEBSITE_HOSTNAME=finance-tracker-manual.northeurope.azurecontainer.io \
    AZURE_POSTGRESQL_HOST=10xdev-finance-tracker-db.postgres.database.azure.com \
    AZURE_POSTGRESQL_NAME=financetracker \
    AZURE_POSTGRESQL_USER=financeadmin \
    AZURE_POSTGRESQL_PASSWORD="YourSecurePassword123!" \
  --restart-policy OnFailure
```

## 📱 Monitoring and Maintenance

### View Container Logs
```bash
# View live logs
az container logs \
  --resource-group finance-tracker-rg \
  --name finance-tracker-container \
  --follow

# View container details
az container show \
  --resource-group finance-tracker-rg \
  --name finance-tracker-container
```

### Update Application
1. Push changes to `main` branch
2. GitHub Actions will automatically rebuild and redeploy
3. Zero-downtime deployment with staging → production flow

### Database Backup
```bash
# Create database backup
az postgres flexible-server backup restore \
  --resource-group finance-tracker-rg \
  --name 10xdev-finance-tracker-db \
  --target-server-name 10xdev-finance-tracker-db-backup \
  --restore-time "2024-01-01T00:00:00Z"
```

## 🔒 Security Best Practices

1. **Secrets Management:**
   - All sensitive data is in GitHub secrets
   - No hardcoded passwords in code
   - Regular secret rotation

2. **Container Security:**
   - Multi-stage Docker builds
   - Non-root user in container
   - Vulnerability scanning with Trivy
   - Regular base image updates

3. **Database Security:**
   - Firewall rules configured
   - SSL connections enforced
   - Regular backups

4. **Network Security:**
   - Container instances in private network (optional)
   - HTTPS enforcement in production

## 🚨 Troubleshooting

### Common Issues:

1. **Container won't start:**
   ```bash
   # Check container logs
   az container logs --resource-group finance-tracker-rg --name finance-tracker-container
   ```

2. **Database connection errors:**
   ```bash
   # Test database connectivity
   az postgres flexible-server connect \
     --name 10xdev-finance-tracker-db \
     --admin-user financeadmin \
     --admin-password "YourSecurePassword123!"
   ```

3. **Image build failures:**
   ```bash
   # Build locally to test
   docker build -t finance-tracker .
   ```

4. **GitHub Actions failures:**
   - Check secrets are correctly configured
   - Verify Azure credentials are valid
   - Check repository permissions

### Health Check Endpoints:
- **Application Health:** `/health/`
- **Database Health:** `/admin/` (login required)

## 🎯 Next Steps

1. **Custom Domain:** Configure custom domain with Azure DNS
2. **HTTPS:** Add SSL certificate with Azure Application Gateway
3. **Monitoring:** Set up Azure Monitor and Application Insights
4. **Scaling:** Configure auto-scaling based on CPU/memory usage
5. **Backup Strategy:** Automated database backups with Azure Backup

## 📞 Support

If you encounter issues:
1. Check container logs: `az container logs`
2. Verify database connectivity
3. Review GitHub Actions logs
4. Check Azure portal for resource status

**Deployment Complete! 🎉**

Your Finance Tracker is now running on Azure with full CI/CD automation!