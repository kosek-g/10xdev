# GitHub Secrets Setup Guide

This document explains how to set up the required GitHub secrets for the CI/CD pipeline.

## Required Secrets

Add these secrets in your GitHub repository: `Settings > Secrets and variables > Actions > New repository secret`

### 1. Azure Credentials
```
Name: AZURE_CREDENTIALS
Value: {
  "clientId": "your-service-principal-client-id",
  "clientSecret": "your-service-principal-client-secret",
  "subscriptionId": "your-azure-subscription-id",
  "tenantId": "your-azure-tenant-id"
}
```

### 2. Azure Container Registry
```
Name: AZURE_CONTAINER_REGISTRY_NAME
Value: your-registry-name

Name: AZURE_CONTAINER_REGISTRY_USERNAME
Value: your-registry-username

Name: AZURE_CONTAINER_REGISTRY_PASSWORD
Value: your-registry-password
```

### 3. Azure Resource Information
```
Name: AZURE_RESOURCE_GROUP
Value: finance-tracker-rg

Name: AZURE_CONTAINER_GROUP
Value: finance-tracker-container
```

### 4. Django Configuration
```
Name: DJANGO_SECRET_KEY
Value: your-very-secure-secret-key-here-make-it-long-and-random

Name: AZURE_POSTGRESQL_HOST
Value: your-postgres-server.postgres.database.azure.com

Name: AZURE_POSTGRESQL_NAME
Value: financetracker

Name: AZURE_POSTGRESQL_USER
Value: financeadmin@your-postgres-server

Name: AZURE_POSTGRESQL_PASSWORD
Value: your-database-password
```

## Setup Instructions

### Step 1: Create Azure Service Principal

1. **Login to Azure CLI:**
   ```bash
   az login
   ```

2. **Create Service Principal:**
   ```bash
   az ad sp create-for-rbac \
     --name "finance-tracker-github-actions" \
     --role contributor \
     --scopes /subscriptions/YOUR_SUBSCRIPTION_ID \
     --sdk-auth
   ```

3. **Copy the JSON output to `AZURE_CREDENTIALS` secret**

### Step 2: Create Azure Container Registry

1. **Create Container Registry:**
   ```bash
   az acr create \
     --resource-group finance-tracker-rg \
     --name financetracker \
     --sku Basic \
     --admin-enabled true
   ```

2. **Get Registry Credentials:**
   ```bash
   az acr credential show --name financetracker
   ```

3. **Add credentials to GitHub secrets:**
   - `AZURE_CONTAINER_REGISTRY_NAME`: `financetracker`
   - `AZURE_CONTAINER_REGISTRY_USERNAME`: (from above command)
   - `AZURE_CONTAINER_REGISTRY_PASSWORD`: (from above command)

### Step 3: Create PostgreSQL Database

1. **Create PostgreSQL Server:**
   ```bash
   az postgres server create \
     --resource-group finance-tracker-rg \
     --name finance-tracker-db \
     --location eastus \
     --admin-user financeadmin \
     --admin-password "YourSecurePassword123!" \
     --sku-name B_Gen5_1 \
     --version 11
   ```

2. **Create Database:**
   ```bash
   az postgres db create \
     --resource-group finance-tracker-rg \
     --server-name finance-tracker-db \
     --name financetracker
   ```

3. **Configure Firewall:**
   ```bash
   az postgres server firewall-rule create \
     --resource-group finance-tracker-rg \
     --server finance-tracker-db \
     --name AllowAzureServices \
     --start-ip-address 0.0.0.0 \
     --end-ip-address 0.0.0.0
   ```

### Step 4: Generate Django Secret Key

```python
# Run this Python code to generate a secure secret key
import secrets
import string

alphabet = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
secret_key = ''.join(secrets.choice(alphabet) for i in range(50))
print(f"DJANGO_SECRET_KEY: {secret_key}")
```

### Step 5: Set GitHub Environments

1. Go to your repository on GitHub
2. Navigate to `Settings > Environments`
3. Create two environments:
   - `staging`
   - `production`
4. (Optional) Add protection rules for production environment

## Environment Variables for Local Development

Create `.env.local` file (DO NOT commit this file):

```bash
# Local Development Environment Variables
SECRET_KEY=your-local-development-secret-key
DEBUG=True
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# For testing with PostgreSQL locally
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=financetracker_local
# DB_USER=postgres
# DB_PASSWORD=postgres
# DB_HOST=localhost
# DB_PORT=5432
```

## Validation

After setting up all secrets, you can validate by:

1. **Push to main branch** to trigger the CI/CD pipeline
2. **Check Actions tab** in your GitHub repository
3. **Monitor the workflow** for any errors
4. **Test the deployed application** at the provided URLs

## Security Best Practices

1. **Rotate secrets regularly** (every 90 days)
2. **Use least privilege principle** for service principals
3. **Monitor access logs** in Azure
4. **Enable Azure Security Center** recommendations
5. **Use Azure Key Vault** for production secrets (advanced)

## Troubleshooting

### Common Issues:

1. **Authentication failed:**
   - Verify service principal credentials
   - Check subscription ID and tenant ID

2. **Container registry push failed:**
   - Verify registry credentials
   - Check registry exists and admin is enabled

3. **Database connection failed:**
   - Verify PostgreSQL server is running
   - Check firewall rules
   - Validate connection string format

4. **Deployment timeout:**
   - Check container resource limits
   - Monitor Azure Container Instances logs

### Useful Commands:

```bash
# Test Azure login
az account show

# Test container registry login
az acr login --name financetracker

# Check container group status
az container show \
  --resource-group finance-tracker-rg \
  --name finance-tracker-container

# View container logs
az container logs \
  --resource-group finance-tracker-rg \
  --name finance-tracker-container
```