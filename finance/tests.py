from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import datetime, date, timedelta
from decimal import Decimal
from .models import Category, Transaction, Budget
from .forms import CategoryForm, TransactionForm, BudgetForm, CustomUserCreationForm


class FinanceModelTests(TestCase):
    """Comprehensive test suite for finance application models"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        
        self.category_income = Category.objects.create(
            user=self.user,
            name='Salary',
            description='Monthly salary'
        )
        
        self.category_expense = Category.objects.create(
            user=self.user,
            name='Groceries',
            description='Food and household items'
        )
        
    def test_category_creation(self):
        """Test category model creation and validation"""
        self.assertEqual(self.category_income.name, 'Salary')
        self.assertEqual(self.category_income.user, self.user)
        self.assertEqual(str(self.category_income), 'Salary (testuser)')
        self.assertTrue(self.category_income.created_at)
        
    def test_category_unique_constraint(self):
        """Test that category names must be unique per user"""
        # Should allow same category name for different users
        Category.objects.create(
            user=self.other_user,
            name='Salary',
            description='Other user salary'
        )
        
        # Should not allow duplicate category name for same user
        with self.assertRaises(Exception):
            Category.objects.create(
                user=self.user,
                name='Salary',
                description='Duplicate category'
            )
        
    def test_transaction_creation(self):
        """Test transaction model creation and validation"""
        transaction = Transaction.objects.create(
            user=self.user,
            type='Income',
            amount=Decimal('3000.00'),
            date=date.today(),
            category=self.category_income,
            description='Monthly salary payment'
        )
        
        self.assertEqual(transaction.amount, Decimal('3000.00'))
        self.assertEqual(transaction.type, 'Income')
        self.assertEqual(transaction.user, self.user)
        self.assertEqual(transaction.category, self.category_income)
        self.assertTrue('Income: 3000.00' in str(transaction))
        self.assertTrue(transaction.created_at)
        self.assertTrue(transaction.updated_at)
        
    def test_transaction_amount_validation(self):
        """Test transaction amount must be positive"""
        with self.assertRaises(ValidationError):
            transaction = Transaction(
                user=self.user,
                type='Expense',
                amount=Decimal('-100.00'),
                date=date.today(),
                category=self.category_expense,
                description='Invalid negative amount'
            )
            transaction.full_clean()
            
    def test_budget_creation(self):
        """Test budget model creation and validation"""
        budget = Budget.objects.create(
            user=self.user,
            category=self.category_expense,
            limit=Decimal('500.00'),
            period='Monthly'
        )
        
        self.assertEqual(budget.limit, Decimal('500.00'))
        self.assertEqual(budget.period, 'Monthly')
        self.assertEqual(budget.user, self.user)
        self.assertEqual(budget.category, self.category_expense)
        
    def test_budget_spending_percentage(self):
        """Test budget spending percentage calculation method"""
        budget = Budget.objects.create(
            user=self.user,
            category=self.category_expense,
            limit=Decimal('500.00'),
            period='Monthly'
        )
        
        # Create test transactions
        Transaction.objects.create(
            user=self.user,
            type='Expense',
            amount=Decimal('150.00'),
            date=date.today(),
            category=self.category_expense,
            description='Groceries 1'
        )
        
        Transaction.objects.create(
            user=self.user,
            type='Expense',
            amount=Decimal('100.00'),
            date=date.today(),
            category=self.category_expense,
            description='Groceries 2'
        )
        
        # Test percentage calculation
        start_date = date.today()
        end_date = date.today()
        percentage = budget.get_spending_percentage(start_date, end_date)
        
        # 250 / 500 * 100 = 50%
        self.assertEqual(percentage, 50.0)


class DashboardBusinessLogicTests(TestCase):
    """Test core business logic calculations on dashboard"""
    
    def setUp(self):
        """Set up test data for business logic tests"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create categories
        self.salary_category = Category.objects.create(
            user=self.user,
            name='Salary',
            description='Monthly salary'
        )
        
        self.groceries_category = Category.objects.create(
            user=self.user,
            name='Groceries',
            description='Food expenses'
        )
        
        self.rent_category = Category.objects.create(
            user=self.user,
            name='Rent',
            description='Monthly rent'
        )
        
        # Get current month/year for testing
        self.current_date = timezone.now().date()
        self.current_month = self.current_date.month
        self.current_year = self.current_date.year
        
    def test_monthly_balance_calculation(self):
        """
        Test that monthly balance is correctly calculated as Income - Expenses
        This is the mandatory test case as specified in requirements
        """
        # Create income transaction
        Transaction.objects.create(
            user=self.user,
            type='Income',
            amount=Decimal('3000.00'),
            date=self.current_date,
            category=self.salary_category,
            description='Monthly salary'
        )
        
        # Create expense transactions
        Transaction.objects.create(
            user=self.user,
            type='Expense',
            amount=Decimal('200.00'),
            date=self.current_date,
            category=self.groceries_category,
            description='Weekly groceries'
        )
        
        Transaction.objects.create(
            user=self.user,
            type='Expense',
            amount=Decimal('1200.00'),
            date=self.current_date,
            category=self.rent_category,
            description='Monthly rent'
        )
        
        # Calculate monthly totals (simulating dashboard logic)
        from django.db.models import Sum
        monthly_transactions = Transaction.objects.filter(
            user=self.user,
            date__month=self.current_month,
            date__year=self.current_year
        )
        
        total_income = monthly_transactions.filter(type='Income').aggregate(
            total=Sum('amount')
        )['total'] or Decimal('0.00')
        
        total_expenses = monthly_transactions.filter(type='Expense').aggregate(
            total=Sum('amount')
        )['total'] or Decimal('0.00')
        
        current_balance = total_income - total_expenses
        
        # Assertions
        self.assertEqual(total_income, Decimal('3000.00'))
        self.assertEqual(total_expenses, Decimal('1400.00'))
        self.assertEqual(current_balance, Decimal('1600.00'))
        
    def test_monthly_calculation_different_months(self):
        """Test that monthly calculations only include current month data"""
        # Create transaction in current month
        Transaction.objects.create(
            user=self.user,
            type='Income',
            amount=Decimal('3000.00'),
            date=self.current_date,
            category=self.salary_category,
            description='Current month salary'
        )
        
        # Create transaction in previous month
        previous_month_date = self.current_date - timedelta(days=40)
        Transaction.objects.create(
            user=self.user,
            type='Income',
            amount=Decimal('2500.00'),
            date=previous_month_date,
            category=self.salary_category,
            description='Previous month salary'
        )
        
        # Calculate only current month
        from django.db.models import Sum
        monthly_transactions = Transaction.objects.filter(
            user=self.user,
            date__month=self.current_month,
            date__year=self.current_year
        )
        
        total_income = monthly_transactions.filter(type='Income').aggregate(
            total=Sum('amount')
        )['total'] or Decimal('0.00')
        
        # Should only include current month transaction
        self.assertEqual(total_income, Decimal('3000.00'))
        
    def test_multiple_users_data_separation(self):
        """Test that users can only see their own financial data"""
        # Create another user
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        
        # Create category and transaction for other user
        other_category = Category.objects.create(
            user=other_user,
            name='Other Salary',
            description='Other user salary'
        )
        
        Transaction.objects.create(
            user=other_user,
            type='Income',
            amount=Decimal('5000.00'),
            date=self.current_date,
            category=other_category,
            description='Other user income'
        )
        
        # Create transaction for first user
        Transaction.objects.create(
            user=self.user,
            type='Income',
            amount=Decimal('3000.00'),
            date=self.current_date,
            category=self.salary_category,
            description='First user income'
        )
        
        # Test that each user only sees their own transactions
        user1_transactions = Transaction.objects.filter(user=self.user)
        user2_transactions = Transaction.objects.filter(user=other_user)
        
        self.assertEqual(user1_transactions.count(), 1)
        self.assertEqual(user2_transactions.count(), 1)
        self.assertEqual(user1_transactions.first().amount, Decimal('3000.00'))
        self.assertEqual(user2_transactions.first().amount, Decimal('5000.00'))


class FormValidationTests(TestCase):
    """Test form validation and functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.category = Category.objects.create(
            user=self.user,
            name='Test Category',
            description='Test description'
        )
        
    def test_custom_user_creation_form(self):
        """Test custom user registration form"""
        form_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        }
        
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        user = form.save()
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.first_name, 'New')
        self.assertEqual(user.last_name, 'User')
        self.assertEqual(user.email, 'newuser@example.com')
        
    def test_category_form_validation(self):
        """Test category form validation"""
        form_data = {
            'name': 'New Category',
            'description': 'New category description'
        }
        
        form = CategoryForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())
        
        # Test duplicate category name
        form_data['name'] = 'Test Category'  # Already exists
        form = CategoryForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('You already have a category with this name.', form.errors['name'])
        
    def test_transaction_form_validation(self):
        """Test transaction form validation"""
        form_data = {
            'type': 'Income',
            'amount': '1500.00',
            'date': '2025-09-29',
            'category': self.category.id,
            'description': 'Test transaction'
        }
        
        form = TransactionForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())
        
    def test_budget_form_validation(self):
        """Test budget form validation"""
        form_data = {
            'category': self.category.id,
            'limit': '500.00',
            'period': 'Monthly'
        }
        
        form = BudgetForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())


class ViewAccessControlTests(TestCase):
    """Test access control and authentication requirements"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.category = Category.objects.create(
            user=self.user,
            name='Test Category',
            description='Test description'
        )
        
    def test_dashboard_requires_login(self):
        """Test that dashboard redirects unauthenticated users to login"""
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, '/accounts/login/?next=/')
        
    def test_transaction_list_requires_login(self):
        """Test that transaction list requires authentication"""
        response = self.client.get(reverse('transaction-list'))
        self.assertRedirects(response, '/accounts/login/?next=/transactions/')
        
    def test_authenticated_user_can_access_dashboard(self):
        """Test that authenticated users can access dashboard"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard')
        
    def test_transaction_creation_requires_login(self):
        """Test that transaction creation requires authentication"""
        response = self.client.get(reverse('transaction-create'))
        self.assertRedirects(response, '/accounts/login/?next=/transactions/create/')
        
    def test_user_can_only_access_own_data(self):
        """Test that users can only access their own transaction data"""
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        
        other_category = Category.objects.create(
            user=other_user,
            name='Other Category',
            description='Other description'
        )
        
        other_transaction = Transaction.objects.create(
            user=other_user,
            type='Income',
            amount=Decimal('1000.00'),
            date=date.today(),
            category=other_category,
            description='Other user transaction'
        )
        
        # Login as first user
        self.client.login(username='testuser', password='testpass123')
        
        # Try to access other user's transaction edit page
        response = self.client.get(reverse('transaction-edit', kwargs={'pk': other_transaction.pk}))
        self.assertEqual(response.status_code, 404)  # Should not be found for this user


class IntegrationTests(TestCase):
    """Integration tests for complete user workflows"""
    
    def setUp(self):
        self.client = Client()
        
    def test_complete_user_registration_workflow(self):
        """Test complete user registration and initial setup workflow"""
        # Register new user
        registration_data = {
            'username': 'integrationuser',
            'first_name': 'Integration',
            'last_name': 'Test',
            'email': 'integration@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        }
        
        response = self.client.post(reverse('register'), data=registration_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        
        # Check user was created
        user = User.objects.get(username='integrationuser')
        self.assertEqual(user.first_name, 'Integration')
        self.assertEqual(user.email, 'integration@example.com')
        
        # Check default categories were created
        default_categories = Category.objects.filter(user=user)
        self.assertEqual(default_categories.count(), 5)
        category_names = [cat.name for cat in default_categories]
        self.assertIn('Salary', category_names)
        self.assertIn('Groceries', category_names)
        
    def test_transaction_and_budget_workflow(self):
        """Test creating transactions and budgets workflow"""
        # Create and login user
        user = User.objects.create_user(
            username='workflowuser',
            email='workflow@example.com',
            password='testpass123'
        )
        self.client.login(username='workflowuser', password='testpass123')
        
        # Create category
        category_data = {
            'name': 'Entertainment',
            'description': 'Movies and fun activities'
        }
        response = self.client.post(reverse('category-create'), data=category_data)
        self.assertEqual(response.status_code, 302)
        
        category = Category.objects.get(user=user, name='Entertainment')
        
        # Create transaction
        transaction_data = {
            'type': 'Expense',
            'amount': '50.00',
            'date': '2025-09-29',
            'category': category.id,
            'description': 'Movie tickets'
        }
        response = self.client.post(reverse('transaction-create'), data=transaction_data)
        self.assertEqual(response.status_code, 302)
        
        # Verify transaction was created
        transaction = Transaction.objects.get(user=user, description='Movie tickets')
        self.assertEqual(transaction.amount, Decimal('50.00'))
        self.assertEqual(transaction.type, 'Expense')
        
        # Create budget
        budget_data = {
            'category': category.id,
            'limit': '200.00',
            'period': 'Monthly'
        }
        response = self.client.post(reverse('budget-create'), data=budget_data)
        self.assertEqual(response.status_code, 302)
        
        # Verify budget was created
        budget = Budget.objects.get(user=user, category=category)
        self.assertEqual(budget.limit, Decimal('200.00'))
        
        # Test dashboard shows correct data
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Movie tickets')
        self.assertContains(response, 'Entertainment')


class PerformanceTests(TestCase):
    """Basic performance and efficiency tests"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='perfuser',
            email='perf@example.com',
            password='testpass123'
        )
        
        self.category = Category.objects.create(
            user=self.user,
            name='Performance Test',
            description='Performance testing category'
        )
        
    def test_large_transaction_dataset_performance(self):
        """Test performance with larger dataset"""
        # Create multiple transactions
        transactions = []
        for i in range(100):
            transactions.append(Transaction(
                user=self.user,
                type='Expense' if i % 2 == 0 else 'Income',
                amount=Decimal(f'{(i + 1) * 10}.00'),
                date=date.today(),
                category=self.category,
                description=f'Transaction {i + 1}'
            ))
        
        Transaction.objects.bulk_create(transactions)
        
        # Test that queries are still efficient
        from django.db.models import Sum
        total_income = Transaction.objects.filter(
            user=self.user,
            type='Income'
        ).aggregate(total=Sum('amount'))['total']
        
        total_expenses = Transaction.objects.filter(
            user=self.user,
            type='Expense'
        ).aggregate(total=Sum('amount'))['total']
        
        self.assertIsNotNone(total_income)
        self.assertIsNotNone(total_expenses)
        self.assertEqual(Transaction.objects.filter(user=self.user).count(), 100)
