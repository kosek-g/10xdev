# 💰 Finance Tracker

A modern, cloud-native personal finance management application built with Django and deployed on Azure Container Apps.

[![CI/CD Pipeline](https://github.com/kosek-g/10xdev/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/kosek-g/10xdev/actions/workflows/ci-cd.yml)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/django-5.2.6-green.svg)](https://djangoproject.com)
[![Azure](https://img.shields.io/badge/azure-container_apps-blue.svg)](https://azure.microsoft.com/en-us/services/container-apps/)

## 🌟 Features

### 💸 Transaction Management
- **Income & Expense Tracking**: Record all your financial transactions with detailed categorization
- **Smart Categories**: Organize transactions with custom categories for better insights
- **Real-time Balance**: Instantly see your current financial position

### 📊 Budget Planning & Analytics
- **Budget Creation**: Set spending limits for different categories
- **Budget Monitoring**: Track progress with visual progress bars and alerts
- **Overspend Alerts**: Get notified when you exceed category budgets
- **Expense Analysis**: View top spending categories and patterns

### 🎨 Modern UI/UX
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Custom Color Scheme**: Professional design with intuitive color coding
- **Bootstrap 5**: Clean, modern interface with smooth interactions
- **Dark Navigation**: Sleek dark grey navigation bar

### 🔐 Security & Authentication
- **User Authentication**: Secure login/logout system
- **Data Privacy**: Each user's financial data is completely isolated
- **Session Management**: Secure session handling

## 🚀 Live Demo

- **Production**: [https://finance-tracker-prod.blackdune-24f7be94.eastus.azurecontainerapps.io](https://finance-tracker-prod.blackdune-24f7be94.eastus.azurecontainerapps.io)
- **Staging**: [https://finance-tracker-staging.blackdune-24f7be94.eastus.azurecontainerapps.io](https://finance-tracker-staging.blackdune-24f7be94.eastus.azurecontainerapps.io)

## 🛠️ Technology Stack

### Backend
- **Django 5.2.6**: High-level Python web framework
- **PostgreSQL**: Robust relational database with Azure Flexible Server
- **Django REST Framework**: API development (extensible)

### Frontend
- **Bootstrap 5**: Responsive CSS framework
- **Bootstrap Icons**: Comprehensive icon library
- **Vanilla JavaScript**: Lightweight client-side interactions

### DevOps & Infrastructure
- **Azure Container Apps**: Serverless container hosting with auto-scaling
- **Azure Container Registry**: Private container image registry
- **GitHub Actions**: Automated CI/CD pipeline
- **Docker**: Containerized deployment

### Development Tools
- **Gunicorn**: Production WSGI server
- **Coverage.py**: Test coverage reporting
- **Bandit**: Security linting
- **Safety**: Dependency vulnerability scanning

## 📱 Screenshots

### Dashboard Overview
The main dashboard provides a comprehensive view of your financial health:
- **Income/Expense Cards**: Color-coded summary cards with custom styling
- **Net Balance**: Dynamic color coding (positive/negative)
- **Budget Progress**: Visual budget tracking with progress bars
- **Recent Transactions**: Quick access to latest activities
- **Quick Actions**: One-click access to common tasks

### Features Highlights
- **Smart Categorization**: Organize transactions by custom categories
- **Budget Monitoring**: Set limits and track spending patterns
- **Responsive Design**: Perfect experience on any device
- **User-Friendly Interface**: Intuitive navigation and clean design

## 🏗️ Architecture

### Application Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   GitHub Repo   │    │  Azure Container │    │   PostgreSQL    │
│                 │───▶│      Apps        │───▶│  Flexible       │
│  (Source Code)  │    │                  │    │   Server        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │
         ▼                        ▼
┌─────────────────┐    ┌──────────────────┐
│  GitHub Actions │    │  Azure Container │
│   (CI/CD)       │───▶│    Registry      │
│                 │    │                  │
└─────────────────┘    └──────────────────┘
```

### CI/CD Pipeline
1. **Code Push** → Triggers automated pipeline
2. **Testing** → Unit tests, security scans, coverage reports
3. **Build** → Docker image creation and tagging
4. **Registry** → Push to Azure Container Registry
5. **Deploy** → Automated deployment to staging and production
6. **Verification** → Health checks and smoke tests

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL (or use SQLite for development)
- Docker (optional, for containerized development)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/kosek-g/10xdev.git
   cd 10xdev
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   export SECRET_KEY="your-secret-key-here"
   export DEBUG=True
   export DB_ENGINE=django.db.backends.sqlite3
   export DB_NAME=db.sqlite3
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Open http://localhost:8000 in your browser
   - Login with your superuser credentials

### Docker Development (Alternative)

1. **Build and run with Docker**
   ```bash
   docker build -t finance-tracker .
   docker run -p 8000:8000 -e DEBUG=True finance-tracker
   ```

## 🧪 Testing

### Run Test Suite
```bash
# Run all tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

### Security Testing
```bash
# Security vulnerability scan
safety check -r requirements.txt

# Security linting
bandit -r . -f json
```

## 📊 Project Statistics

- **21 Unit Tests**: Comprehensive test coverage
- **Models**: 3 core models (Transaction, Category, Budget)
- **Views**: 15+ functional views
- **Templates**: Responsive, mobile-first design
- **Security**: Automated security scanning and updates

## 🔧 Configuration

### Environment Variables
| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Django secret key | ✅ |
| `DEBUG` | Debug mode (True/False) | ✅ |
| `AZURE_POSTGRESQL_HOST` | Database host | ✅ |
| `AZURE_POSTGRESQL_NAME` | Database name | ✅ |
| `AZURE_POSTGRESQL_USER` | Database user | ✅ |
| `AZURE_POSTGRESQL_PASSWORD` | Database password | ✅ |

### Azure Deployment
The application is configured for automatic deployment to Azure Container Apps with:
- **Auto-scaling**: Scales based on demand (1-5 replicas)
- **Health Checks**: Automated health monitoring
- **Zero-downtime deployments**: Rolling updates
- **SSL/TLS**: Automatic HTTPS certificates

## 📈 Monitoring & Health

### Health Check Endpoint
- **URL**: `/health/`
- **Purpose**: Container health verification
- **Response**: HTTP 200 with "Finance Tracker is healthy!"

### Application Monitoring
- **Azure Monitor**: Integrated application insights
- **Container Logs**: Real-time logging and debugging
- **Performance Metrics**: CPU, memory, and request metrics


### Code Quality
- Follow PEP 8 Python style guidelines
- Add docstrings for new functions and classes
- Maintain test coverage above 80%
- Security scan must pass (bandit, safety)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Grzegorz Kosek**

- Email: kosek.grzegorzz@gmai.com
- GitHub: [@kosek-g](https://github.com/kosek-g)

