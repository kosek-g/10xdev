# PostgreSQL Flexible Server Migration Guide

## 🔄 Migration Summary

Your deployment guides have been updated to use **Azure Database for PostgreSQL Flexible Server** instead of the deprecated Single Server. This is a critical update since Microsoft deprecated Single Server in March 2023.

## 📋 What Changed

### **1. Server Creation Command**
**Before (Deprecated Single Server):**
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

**After (New Flexible Server):**
```bash
az postgres flexible-server create \
  --resource-group finance-tracker-rg \
  --name finance-tracker-db \
  --location eastus \
  --admin-user financeadmin \
  --admin-password "YourSecurePassword123!" \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --storage-size 32 \
  --version 15
```

### **2. Database Creation Command**
**Before:**
```bash
az postgres db create \
  --resource-group finance-tracker-rg \
  --server-name finance-tracker-db \
  --name financetracker
```

**After:**
```bash
az postgres flexible-server db create \
  --resource-group finance-tracker-rg \
  --server-name finance-tracker-db \
  --database-name financetracker
```

### **3. Firewall Rule Command**
**Before:**
```bash
az postgres server firewall-rule create \
  --resource-group finance-tracker-rg \
  --server finance-tracker-db \
  --name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0
```

**After:**
```bash
az postgres flexible-server firewall-rule create \
  --resource-group finance-tracker-rg \
  --name finance-tracker-db \
  --rule-name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0
```

## ✨ Benefits of Flexible Server

### **1. Better Performance**
- **Burstable Tier**: Cost-effective for development and low-traffic applications
- **More SKU Options**: Better price-performance ratio
- **Improved I/O Performance**: Better disk throughput

### **2. Enhanced Features**
- **Zone Redundant High Availability**: Better reliability
- **Major Version Upgrades**: In-place upgrades supported
- **Better Backup Options**: Point-in-time recovery up to 35 days
- **Connection Pooling**: Built-in PgBouncer support

### **3. Modern Architecture**
- **Latest PostgreSQL Versions**: Support for PostgreSQL 15, 16, 17
- **ARM64 Support**: Better performance on modern hardware
- **Improved Monitoring**: Better integration with Azure Monitor

### **4. Cost Optimization**
- **Stop/Start Capability**: Save costs during development
- **Auto-scaling**: Scale compute and storage independently
- **Reserved Instances**: Additional cost savings for production

## 🔧 Updated Configuration

### **Connection String Format**
The connection format remains the same:
```
Host: your-server-name.postgres.database.azure.com
Port: 5432
SSL: Required
```

### **Environment Variables**
No changes needed in your Django application:
```bash
AZURE_POSTGRESQL_HOST=finance-tracker-db.postgres.database.azure.com
AZURE_POSTGRESQL_NAME=financetracker
AZURE_POSTGRESQL_USER=financeadmin@finance-tracker-db  # Note: @ syntax still used
AZURE_POSTGRESQL_PASSWORD=your-password
```

## 📁 Updated Files

1. **`azure-deployment-guide.md`** ✅
2. **`github-secrets-setup.md`** ✅  
3. **`github-actions-deployment-guide.md`** ✅
4. **Django settings files** ✅ (Already compatible)

## 🚀 Migration Steps for Existing Deployments

If you already have a Single Server deployment:

### Option 1: Create New Flexible Server (Recommended)
1. **Create new Flexible Server** using updated commands
2. **Export data** from old server: `pg_dump`
3. **Import data** to new server: `psql`
4. **Update connection strings** in your application
5. **Test thoroughly** before switching traffic
6. **Delete old Single Server** once confirmed working

### Option 2: Use Azure Database Migration Service
1. Use Azure's built-in migration tools
2. Minimal downtime migration
3. Automatic data validation

## 🛠️ Testing Your Setup

Test the new Flexible Server setup:

```bash
# Test server creation
az postgres flexible-server create \
  --resource-group test-rg \
  --name test-server \
  --location eastus \
  --admin-user testuser \
  --admin-password "TestPassword123!" \
  --sku-name Standard_B1ms \
  --tier Burstable

# Test connection
az postgres flexible-server connect \
  --name test-server \
  --admin-user testuser \
  --admin-password "TestPassword123!"

# Cleanup test resources
az postgres flexible-server delete \
  --resource-group test-rg \
  --name test-server \
  --yes
```

## 📊 Cost Comparison

### **Single Server (Deprecated)**
- Basic tier: ~$25/month
- Limited scaling options
- Manual backup management

### **Flexible Server (New)**
- Burstable tier: ~$15/month (with stop/start)
- Auto-scaling capabilities  
- Automated backup and point-in-time recovery
- Better performance per dollar

## 🆘 Troubleshooting

### **Common Migration Issues:**

1. **Authentication Error:**
   - Ensure using correct admin format: `username@servername`
   - Verify firewall rules are configured

2. **Connection Timeout:**
   - Check if server is in stopped state
   - Verify network connectivity and firewall rules

3. **Performance Issues:**
   - Review compute tier selection
   - Consider upgrading from Burstable to General Purpose

4. **SSL Connection Issues:**
   - Ensure `sslmode=require` in connection string
   - Download and configure SSL certificate if needed

## 📚 Additional Resources

- [Azure PostgreSQL Flexible Server Documentation](https://docs.microsoft.com/en-us/azure/postgresql/flexible-server/)
- [Migration Guide from Single Server](https://docs.microsoft.com/en-us/azure/postgresql/migrate/concepts-single-to-flexible)
- [Performance Best Practices](https://docs.microsoft.com/en-us/azure/postgresql/flexible-server/concepts-performance-recommendations)

---

✅ **Your deployment guides are now updated for PostgreSQL Flexible Server!** 

This ensures your infrastructure uses the latest, supported, and most cost-effective Azure database solution.