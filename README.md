# Finance Tracker - Personal Budgeting Application

A comprehensive Django-based personal finance tracker and budgeting application built for a Software Engineering course focused on AI-driven development. This application helps users track income, expenses, and manage budgets across different categories.

## Features

### ✅ Core Functionality
- **User Authentication**: Secure registration, login, and logout
- **Transaction Management**: Full CRUD operations for income and expense tracking
- **Category Management**: User-specific categories for organizing transactions
- **Budget Tracking**: Set spending limits and monitor budget usage
- **Dashboard Analytics**: Real-time financial overview with balance calculations

### ✅ Technical Requirements Met
- **Django 5.x**: Latest stable Django framework
- **SQLite/PostgreSQL/MySQL Support**: Configurable database backends
- **User Access Control**: All data is user-specific with proper authorization
- **Class-Based Views**: Modern Django CBV implementation
- **Responsive UI**: Bootstrap 5 with crispy forms
- **Comprehensive Testing**: Unit tests for core business logic
- **CI/CD Ready**: Docker containerization and GitHub Actions workflow

## Quick Start

### Prerequisites
- Python 3.12+
- Django 5.x
- Git

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd FinanceTracker
```

2. **Set up virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Create superuser (optional)**
```bash
python manage.py createsuperuser
```

6. **Start development server**
```bash
python manage.py runserver
```

7. **Access the application**
- Main app: http://localhost:8000/
- Admin panel: http://localhost:8000/admin/

## Usage

### Getting Started
1. **Register**: Create a new account at `/register/`
2. **Add Categories**: Create categories like "Salary", "Groceries", "Entertainment"
3. **Record Transactions**: Add your income and expenses
4. **Set Budgets**: Define spending limits for categories
5. **Monitor Dashboard**: View your financial overview and budget progress

### Core Workflows

**Adding a Transaction:**
1. Navigate to "Add Transaction"
2. Select type (Income/Expense)
3. Enter amount, date, category, and description
4. Save to update your financial records

**Budget Management:**
1. Go to "Budgets" section
2. Create budgets for specific categories
3. Set spending limits and time periods
4. Monitor usage on the dashboard

## Architecture

### Models
- **Category**: User-specific transaction categories
- **Transaction**: Income and expense records with user association
- **Budget**: Spending limits per category with usage tracking

### Views
- **Dashboard**: Financial summary with business logic calculations
- **Transaction CRUD**: Complete transaction management
- **Category Management**: User category organization
- **Budget Tracking**: Budget creation and monitoring

### Security Features
- User authentication required for all financial views
- Data isolation (users can only access their own data)
- CSRF protection on all forms
- Secure password handling

## Testing

Run the test suite:
```bash
python manage.py test finance
```

The test suite includes:
- Model validation tests
- Core business logic verification (monthly balance calculation)
- User access control verification
- Authentication requirement tests

## Docker Support

### Build and run with Docker:
```bash
# Build the image
docker build -t financetracker .

# Run the container
docker run -p 8000:8000 financetracker
```

### Environment Variables for Production:
```bash
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DATABASE_ENGINE=postgresql  # or mysql
DATABASE_NAME=financetracker
DATABASE_USER=your-db-user
DATABASE_PASSWORD=your-db-password
DATABASE_HOST=your-db-host
DATABASE_PORT=5432
```

## CI/CD Pipeline

The project includes a GitHub Actions workflow (`.github/workflows/django.yml`) that:

1. **Tests**: Runs unit tests with PostgreSQL
2. **Build**: Creates Docker image
3. **Validation**: Performs basic health checks
4. **Deploy**: (Template for production deployment)

## Database Configuration

### SQLite (Default - Development)
No additional configuration needed. Database file: `db.sqlite3`

### PostgreSQL (Production)
```bash
export DATABASE_ENGINE=postgresql
export DATABASE_NAME=financetracker
export DATABASE_USER=postgres
export DATABASE_PASSWORD=your_password
export DATABASE_HOST=localhost
export DATABASE_PORT=5432
```

### MySQL (Production)
```bash
export DATABASE_ENGINE=mysql
export DATABASE_NAME=financetracker
export DATABASE_USER=root
export DATABASE_PASSWORD=your_password
export DATABASE_HOST=localhost
export DATABASE_PORT=3306
```

## Project Structure

```
FinanceTracker/
├── FinanceTracker/          # Project configuration
│   ├── settings.py          # Django settings with environment support
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── finance/                 # Main application
│   ├── models.py            # Category, Transaction, Budget models
│   ├── views.py             # CBVs and dashboard logic
│   ├── forms.py             # Django forms with crispy styling
│   ├── urls.py              # App URL patterns
│   ├── admin.py             # Admin interface configuration
│   └── tests.py             # Comprehensive test suite
├── templates/               # Django templates
│   ├── base.html            # Base template with Bootstrap
│   ├── registration/        # Auth templates
│   └── finance/             # App-specific templates
├── requirements.txt         # Python dependencies
├── Dockerfile              # Container configuration
└── .github/workflows/      # CI/CD pipeline
```

## Contributing

This project was developed as part of a Software Engineering course assignment focusing on AI-assisted development practices. The implementation demonstrates:

- Modern Django development patterns
- Comprehensive testing strategies
- CI/CD best practices
- Security-first approach
- Responsive UI design

## License

This project is developed for educational purposes as part of a Software Engineering course assignment.

---

**Built with Django 5.x | Bootstrap 5 | Docker | CI/CD Ready**