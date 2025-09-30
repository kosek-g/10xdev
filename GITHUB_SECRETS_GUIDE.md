# GitHub Secrets Configuration Guide

## 🔐 Complete GitHub Secrets Setup for Docker Deployment

This document provides the exact secrets configuration needed for your CI/CD pipeline.

## 📍 Where to Add Secrets

1. Go to your GitHub repository: `https://github.com/kosek-g/10xdev`
2. Click **Settings** tab
3. Click **Secrets and variables** → **Actions**
4. Click **New repository secret**

## 🔑 Required Secrets List

### 1. Azure Authentication
```
Secret Name: AZURE_CREDENTIALS
Value: {
  "clientId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "clientSecret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "subscriptionId": "fa0b8e00-271b-498d-8c48-975518312f0e",
  "tenantId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```
**How to get:** Copy the COMPLETE JSON output from this command:
```bash
az ad sp create-for-rbac \
  --name "finance-tracker-github-actions" \
  --role contributor \
  --scopes /subscriptions/fa0b8e00-271b-498d-8c48-975518312f0e \
  --sdk-auth
```

### 2. Container Registry Secrets

```
Secret Name: AZURE_CONTAINER_REGISTRY_NAME
Value: financetracker10xdev
```

```
Secret Name: AZURE_CONTAINER_REGISTRY_USERNAME
Value: financetracker10xdev
```

```
Secret Name: AZURE_CONTAINER_REGISTRY_PASSWORD
Value: [password from ACR credentials]
```
**How to get password:**
```bash
az acr credential show \
  --name financetracker10xdev \
  --resource-group finance-tracker-rg
```
Copy the `password` field from the output.

### 3. Azure Resource Configuration

```
Secret Name: AZURE_RESOURCE_GROUP
Value: finance-tracker-rg
```

```
Secret Name: AZURE_CONTAINER_GROUP
Value: finance-tracker-container
```

### 4. Django Application Secrets

```
Secret Name: DJANGO_SECRET_KEY
Value: [50-character random secret key]
```
**How to generate:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Example output: `django-insecure-xyz123abc456def789ghi012jkl345mno678pqr901stu234vwx567`

### 5. Database Connection Secrets

```
Secret Name: AZURE_POSTGRESQL_HOST
Value: 10xdev-finance-tracker-db.postgres.database.azure.com
```

```
Secret Name: AZURE_POSTGRESQL_NAME
Value: financetracker
```

```
Secret Name: AZURE_POSTGRESQL_USER
Value: financeadmin
```

```
Secret Name: AZURE_POSTGRESQL_PASSWORD
Value: YourSecurePassword123!
```

## 📋 Complete Secrets Checklist

- [ ] `AZURE_CREDENTIALS` (JSON from service principal)
- [ ] `AZURE_CONTAINER_REGISTRY_NAME` (financetracker10xdev)
- [ ] `AZURE_CONTAINER_REGISTRY_USERNAME` (financetracker10xdev)
- [ ] `AZURE_CONTAINER_REGISTRY_PASSWORD` (from ACR credentials)
- [ ] `AZURE_RESOURCE_GROUP` (finance-tracker-rg)
- [ ] `AZURE_CONTAINER_GROUP` (finance-tracker-container)
- [ ] `DJANGO_SECRET_KEY` (generated 50-char key)
- [ ] `AZURE_POSTGRESQL_HOST` (database hostname)
- [ ] `AZURE_POSTGRESQL_NAME` (financetracker)
- [ ] `AZURE_POSTGRESQL_USER` (financeadmin)
- [ ] `AZURE_POSTGRESQL_PASSWORD` (database password)

## 🔍 How to Verify Secrets

After adding all secrets, you can verify them by:

1. Going to your repository's **Actions** tab
2. Triggering a new workflow run by pushing to `main` branch
3. Checking the workflow logs for authentication errors

## 🚨 Security Notes

1. **Never commit secrets to code** - They should only exist in GitHub secrets
2. **Rotate secrets regularly** - Especially the service principal credentials
3. **Use strong passwords** - For database and Django secret key
4. **Monitor access** - Check GitHub audit logs for secret access

## 🔄 Updating Secrets

If you need to update secrets later:

1. **Database Password:**
   ```bash
   # Update database password
   az postgres flexible-server update \
     --resource-group finance-tracker-rg \
     --name 10xdev-finance-tracker-db \
     --admin-password "NewSecurePassword123!"
   
   # Update GitHub secret: AZURE_POSTGRESQL_PASSWORD
   ```

2. **Service Principal Credentials:**
   ```bash
   # Create new service principal (rotate credentials)
   az ad sp create-for-rbac \
     --name "finance-tracker-github-actions-new" \
     --role contributor \
     --scopes /subscriptions/fa0b8e00-271b-498d-8c48-975518312f0e \
     --sdk-auth
   
   # Update GitHub secret: AZURE_CREDENTIALS
   ```

3. **Container Registry Password:**
   ```bash
   # Regenerate ACR password
   az acr credential renew \
     --name financetracker10xdev \
     --password-name password
   
   # Get new password
   az acr credential show \
     --name financetracker10xdev \
     --resource-group finance-tracker-rg
   
   # Update GitHub secret: AZURE_CONTAINER_REGISTRY_PASSWORD
   ```

## ✅ Testing Secrets Configuration

Once all secrets are configured, test by pushing a commit to main:

```bash
git add .
git commit -m "Test CI/CD with Docker deployment"
git push origin main
```

Watch the GitHub Actions workflow to ensure all steps complete successfully.

## 🛠️ Troubleshooting Secrets

### Common Issues:

1. **Invalid JSON in AZURE_CREDENTIALS:**
   - Ensure the JSON is valid (no trailing commas, proper quotes)
   - Copy the ENTIRE output from the `az ad sp create-for-rbac` command

2. **Container Registry Authentication Failed:**
   - Verify the registry name matches exactly: `financetracker10xdev`
   - Check that admin user is enabled on the registry
   - Ensure password is copied correctly (no extra spaces)

3. **Database Connection Errors:**
   - Verify the hostname format: `servername.postgres.database.azure.com`
   - Check that firewall rules allow Azure services
   - Ensure password matches exactly what was set during creation

4. **Service Principal Permission Errors:**
   - Verify the service principal has `contributor` role
   - Check the subscription ID is correct
   - Ensure the scope includes the full subscription path

### Debug Commands:

```bash
# Test service principal login
az login --service-principal \
  --username "CLIENT_ID" \
  --password "CLIENT_SECRET" \
  --tenant "TENANT_ID"

# Test ACR access
az acr login --name financetracker10xdev

# Test database connection
az postgres flexible-server connect \
  --name 10xdev-finance-tracker-db \
  --admin-user financeadmin \
  --admin-password "YourSecurePassword123!"
```

✅ **All secrets configured correctly = Successful automated deployment!**