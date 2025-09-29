# Azure Deployment Guide for Finance Tracker

## Prerequisites
- Azure subscription
- Azure CLI installed locally
- Git repository (GitHub/Azure DevOps)

## Option 1: Quick Deployment (Recommended)

### Step 1: Create Azure Resources
```bash
# Login to Azure
az login

# Create resource group
az group create --name finance-tracker-rg --location "East US"

# Create Azure Database for PostgreSQL
az postgres server create \
  --resource-group finance-tracker-rg \
  --name finance-tracker-db \
  --location "East US" \
  --admin-user financeadmin \
  --admin-password "YourSecurePassword123!" \
  --sku-name B_Gen5_1

# Create database
az postgres db create \
  --resource-group finance-tracker-rg \
  --server-name finance-tracker-db \
  --name financetracker

# Allow Azure services to access database
az postgres server firewall-rule create \
  --resource-group finance-tracker-rg \
  --server finance-tracker-db \
  --name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0

# Create App Service Plan
az appservice plan create \
  --name finance-tracker-plan \
  --resource-group finance-tracker-rg \
  --sku B1 \
  --is-linux

# Create Web App
az webapp create \
  --resource-group finance-tracker-rg \
  --plan finance-tracker-plan \
  --name finance-tracker-app \
  --runtime "PYTHON|3.11" \
  --deployment-source-url https://github.com/yourusername/finance-tracker.git
```

### Step 2: Configure Environment Variables
```bash
# Set application settings
az webapp config appsettings set \
  --resource-group finance-tracker-rg \
  --name finance-tracker-app \
  --settings \
  DJANGO_SETTINGS_MODULE=FinanceTracker.azure_settings \
  SECRET_KEY="your-very-secure-secret-key-here" \
  DEBUG=False \
  WEBSITE_HOSTNAME=finance-tracker-app.azurewebsites.net \
  AZURE_POSTGRESQL_HOST=finance-tracker-db.postgres.database.azure.com \
  AZURE_POSTGRESQL_NAME=financetracker \
  AZURE_POSTGRESQL_USER=financeadmin@finance-tracker-db \
  AZURE_POSTGRESQL_PASSWORD="YourSecurePassword123!"

# Set startup command
az webapp config set \
  --resource-group finance-tracker-rg \
  --name finance-tracker-app \
  --startup-file "startup.sh"
```

## Option 2: Using Azure Portal

### Step 1: Create Resources in Portal
1. Go to Azure Portal (portal.azure.com)
2. Create Resource Group: `finance-tracker-rg`
3. Create Azure Database for PostgreSQL:
   - Server name: `finance-tracker-db`
   - Admin username: `financeadmin`
   - Location: `East US`
   - Pricing tier: `Basic`
4. Create App Service:
   - Name: `finance-tracker-app`
   - Runtime: `Python 3.11`
   - Operating System: `Linux`
   - Region: `East US`

### Step 2: Configure Database
1. In PostgreSQL server, go to Connection security
2. Add firewall rule for Azure services (0.0.0.0 - 0.0.0.0)
3. Create database named `financetracker`

### Step 3: Deploy Application
1. In App Service, go to Deployment Center
2. Choose your source (GitHub, Azure Repos, etc.)
3. Configure deployment settings

### Step 4: Configure Environment Variables
In App Service → Configuration → Application Settings, add:
- `DJANGO_SETTINGS_MODULE`: `FinanceTracker.azure_settings`
- `SECRET_KEY`: `your-very-secure-secret-key-here`
- `DEBUG`: `False`
- `WEBSITE_HOSTNAME`: `your-app-name.azurewebsites.net`
- `AZURE_POSTGRESQL_HOST`: `your-server.postgres.database.azure.com`
- `AZURE_POSTGRESQL_NAME`: `financetracker`
- `AZURE_POSTGRESQL_USER`: `financeadmin@your-server`
- `AZURE_POSTGRESQL_PASSWORD`: `your-password`

### Step 5: Set Startup Command
In App Service → Configuration → General Settings:
- Startup Command: `startup.sh`

## Option 3: Using Azure Container Instances (Docker)

### Create Dockerfile
Already created in the project root.

### Deploy Container
```bash
# Build and push to Azure Container Registry
az acr create --resource-group finance-tracker-rg --name financetracker --sku Basic
az acr build --registry financetracker --image finance-tracker .

# Create container instance
az container create \
  --resource-group finance-tracker-rg \
  --name finance-tracker-container \
  --image financetracker.azurecr.io/finance-tracker \
  --dns-name-label finance-tracker \
  --ports 8000
```

## Post-Deployment Steps

### 1. Create Superuser
Connect to your app via SSH or use Azure Cloud Shell:
```bash
python manage.py createsuperuser
```

### 2. Verify Deployment
- Visit your app URL
- Test login/registration
- Check admin interface
- Verify database connectivity

### 3. Monitor Application
- Enable Application Insights
- Set up log monitoring
- Configure health checks

## Troubleshooting

### Common Issues
1. **Database Connection Error**: Check firewall rules and connection strings
2. **Static Files Not Loading**: Verify WhiteNoise configuration
3. **500 Internal Server Error**: Check logs in Azure Portal
4. **Migration Errors**: Manually run migrations via SSH

### View Logs
```bash
az webapp log tail --name finance-tracker-app --resource-group finance-tracker-rg
```

## Security Considerations
- Use Azure Key Vault for secrets
- Enable HTTPS only
- Configure CORS if needed
- Set up Azure Active Directory for authentication (optional)
- Enable backup for database

## Cost Optimization
- Use Basic tier for development
- Scale down during non-business hours
- Consider Azure Free Tier limitations
- Monitor resource usage

## Next Steps
- Set up CI/CD pipeline
- Configure custom domain
- Implement Azure Monitor
- Add SSL certificate
- Set up automated backups