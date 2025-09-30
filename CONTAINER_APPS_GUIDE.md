# Azure Container Apps Deployment Guide

## 🚀 Production-Ready Deployment with Azure Container Apps

Azure Container Apps provides enterprise-grade container hosting with automatic scaling, load balancing, and high availability. This guide shows you how to deploy your Finance Tracker application using this modern, serverless container platform.

## ✨ **Why Container Apps vs Container Instances?**

**Azure Container Apps Benefits:**
- ✅ **Production Ready** - Built for enterprise workloads
- ✅ **Auto Scaling** - Scales from 0 to N based on demand
- ✅ **Load Balancing** - Built-in traffic distribution
- ✅ **Health Management** - Automatic restart and self-healing
- ✅ **Blue-Green Deployments** - Zero-downtime updates
- ✅ **HTTPS Termination** - Automatic SSL/TLS certificates
- ✅ **Cost Efficient** - Pay only for what you use

## 📊 **Current Deployment URLs**

- **🌐 Production:** https://finance-tracker-prod.blackdune-24f7be94.eastus.azurecontainerapps.io
- **🧪 Staging:** https://finance-tracker-staging.blackdune-24f7be94.eastus.azurecontainerapps.io

## 🏗️ **Infrastructure Overview**

Your deployment includes:

1. **Container Apps Environment** (`finance-tracker-env`)
   - Shared infrastructure for staging and production
   - Built-in Log Analytics workspace
   - Network isolation and security

2. **Container Apps**
   - `finance-tracker-staging` - For testing deployments
   - `finance-tracker-prod` - Production application

3. **Azure Container Registry** (`financetracker10xdev`)
   - Private Docker image storage
   - Integrated with CI/CD pipeline

4. **PostgreSQL Flexible Server** (`10xdev-finance-tracker-db`)
   - B1ms tier for cost optimization
   - Shared between staging and production

## 🔄 **CI/CD Pipeline Flow**

Your GitHub Actions pipeline now:

1. **Tests** - Runs 21 unit tests with PostgreSQL
2. **Security Scan** - Safety and Bandit security checks
3. **Build & Push** - Creates Docker image and pushes to ACR
4. **Deploy Staging** - Updates staging Container App
5. **Health Checks** - Verifies staging deployment
6. **Deploy Production** - Updates production Container App
7. **Final Verification** - Confirms production health

## 🛠️ **Manual Commands for Container Apps**

### View Application Status
```bash
# Check staging app status
az containerapp show \
  --name finance-tracker-staging \
  --resource-group finance-tracker-rg

# Check production app status
az containerapp show \
  --name finance-tracker-prod \
  --resource-group finance-tracker-rg
```

### View Application Logs
```bash
# Staging logs
az containerapp logs show \
  --name finance-tracker-staging \
  --resource-group finance-tracker-rg \
  --follow

# Production logs
az containerapp logs show \
  --name finance-tracker-prod \
  --resource-group finance-tracker-rg \
  --follow
```

### Manual Deployment Updates
```bash
# Update staging with latest image
az containerapp update \
  --name finance-tracker-staging \
  --resource-group finance-tracker-rg \
  --image financetracker10xdev.azurecr.io/finance-tracker:latest

# Update production with latest image
az containerapp update \
  --name finance-tracker-prod \
  --resource-group finance-tracker-rg \
  --image financetracker10xdev.azurecr.io/finance-tracker:latest
```

### Scale Applications
```bash
# Scale production app (manual)
az containerapp update \
  --name finance-tracker-prod \
  --resource-group finance-tracker-rg \
  --min-replicas 2 \
  --max-replicas 10

# Scale down for cost savings
az containerapp update \
  --name finance-tracker-staging \
  --resource-group finance-tracker-rg \
  --min-replicas 0 \
  --max-replicas 1
```

## 💰 **Cost Optimization**

### Current Monthly Costs (Estimated):
- **PostgreSQL B1ms:** ~$12-17/month (or FREE with Azure credits)
- **Container Registry Basic:** ~$5/month
- **Container Apps:** ~$5-15/month (consumption-based)
- **Log Analytics:** ~$2-5/month
- **Total:** ~$24-42/month

### Money-Saving Strategies:
```bash
# Stop database during development
az postgres flexible-server stop \
  --resource-group finance-tracker-rg \
  --name 10xdev-finance-tracker-db

# Scale staging to zero when not needed
az containerapp update \
  --name finance-tracker-staging \
  --resource-group finance-tracker-rg \
  --min-replicas 0
```

## 🔒 **Security Features**

- **🔐 HTTPS Only** - Automatic SSL/TLS termination
- **🛡️ Private Registry** - Images stored in private ACR
- **🔑 Managed Secrets** - Database credentials securely stored
- **🌐 Network Isolation** - Container Apps environment isolation
- **📊 Audit Logs** - Complete deployment and access logging

## 📈 **Monitoring & Observability**

### Application Health
```bash
# Check health endpoints
curl https://finance-tracker-prod.blackdune-24f7be94.eastus.azurecontainerapps.io/health/
curl https://finance-tracker-staging.blackdune-24f7be94.eastus.azurecontainerapps.io/health/
```

### Performance Metrics
- **Response Times** - Available in Azure portal
- **Request Counts** - Built-in metrics
- **Error Rates** - Automatic tracking
- **Resource Usage** - CPU and memory monitoring

## 🚨 **Troubleshooting**

### Common Issues:

1. **App Not Starting:**
   ```bash
   # Check container logs
   az containerapp logs show --name finance-tracker-prod --resource-group finance-tracker-rg
   ```

2. **Database Connection:**
   ```bash
   # Test database connectivity
   az postgres flexible-server connect \
     --name 10xdev-finance-tracker-db \
     --admin-user financeadmin
   ```

3. **Image Pull Issues:**
   ```bash
   # Verify ACR credentials
   az acr credential show --name financetracker10xdev
   ```

### Health Check Commands:
```bash
# Test all endpoints
curl -I https://finance-tracker-prod.blackdune-24f7be94.eastus.azurecontainerapps.io/
curl -I https://finance-tracker-prod.blackdune-24f7be94.eastus.azurecontainerapps.io/health/
curl -I https://finance-tracker-prod.blackdune-24f7be94.eastus.azurecontainerapps.io/admin/
```

## 🎯 **Next Steps**

1. **Custom Domain** - Add your own domain name
2. **Auto-scaling Rules** - Configure CPU/memory-based scaling
3. **Monitoring Alerts** - Set up Azure Monitor alerts
4. **Backup Strategy** - Automated database backups
5. **Multi-region** - Deploy to multiple Azure regions

## 📞 **Support**

- **Application URL:** https://finance-tracker-prod.blackdune-24f7be94.eastus.azurecontainerapps.io
- **Admin Panel:** https://finance-tracker-prod.blackdune-24f7be94.eastus.azurecontainerapps.io/admin/
- **Health Check:** https://finance-tracker-prod.blackdune-24f7be94.eastus.azurecontainerapps.io/health/

**Your Finance Tracker is now running on enterprise-grade Azure Container Apps! 🎉**