from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import datetime, date
from decimal import Decimal
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import connection
from .models import Transaction, Category, Budget
from .forms import TransactionForm, CategoryForm, BudgetForm, CustomUserCreationForm


class UserAccessMixin(LoginRequiredMixin):
    """Mixin to ensure users can only access their own data"""
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


# Authentication Views
def register_view(request):
    """User registration view"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Finance Tracker.')
            
            # Create default categories for new user
            default_categories = [
                {'name': 'Salary', 'description': 'Monthly salary and wages'},
                {'name': 'Groceries', 'description': 'Food and household items'},
                {'name': 'Transportation', 'description': 'Gas, public transit, car expenses'},
                {'name': 'Entertainment', 'description': 'Movies, dining out, hobbies'},
                {'name': 'Utilities', 'description': 'Electricity, water, internet, phone'},
            ]
            
            for cat_data in default_categories:
                Category.objects.create(user=user, **cat_data)
            
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})


@login_required
def dashboard_view(request):
    """Main dashboard view with financial summary and budget tracking"""
    # Get current month data
    current_date = timezone.now().date()
    current_month = current_date.month
    current_year = current_date.year
    
    # Calculate monthly totals
    monthly_transactions = Transaction.objects.filter(
        user=request.user,
        date__month=current_month,
        date__year=current_year
    )
    
    total_income = monthly_transactions.filter(type='Income').aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0.00')
    
    total_expenses = monthly_transactions.filter(type='Expense').aggregate(
        total=Sum('amount')
    )['total'] or Decimal('0.00')
    
    current_balance = total_income - total_expenses
    
    # Get recent transactions (last 10)
    recent_transactions = Transaction.objects.filter(user=request.user)[:10]
    
    # Get budget information
    monthly_budgets = Budget.objects.filter(user=request.user, period='Monthly')
    budget_data = []
    
    for budget in monthly_budgets:
        spent = monthly_transactions.filter(
            type='Expense',
            category=budget.category
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        percentage = float((spent / budget.limit) * 100) if budget.limit > 0 else 0
        percentage = min(percentage, 100)  # Cap at 100%
        
        budget_data.append({
            'budget': budget,
            'spent': spent,
            'remaining': budget.limit - spent,
            'percentage': percentage,
            'is_over_budget': spent > budget.limit
        })
    
    # Get expense breakdown by category for current month
    expense_breakdown = monthly_transactions.filter(type='Expense').values(
        'category__name'
    ).annotate(
        total=Sum('amount')
    ).order_by('-total')[:5]
    
    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'current_balance': current_balance,
        'recent_transactions': recent_transactions,
        'budget_data': budget_data,
        'expense_breakdown': expense_breakdown,
        'current_month': current_date.strftime('%B %Y'),
    }
    
    return render(request, 'finance/dashboard.html', context)


# Transaction CRUD Views
class TransactionListView(UserAccessMixin, ListView):
    """List all user's transactions"""
    model = Transaction
    template_name = 'finance/transaction_list.html'
    context_object_name = 'transactions'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by transaction type if specified
        transaction_type = self.request.GET.get('type')
        if transaction_type in ['Income', 'Expense']:
            queryset = queryset.filter(type=transaction_type)
        
        # Filter by category if specified
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(user=self.request.user)
        context['selected_type'] = self.request.GET.get('type', '')
        context['selected_category'] = self.request.GET.get('category', '')
        return context


class TransactionCreateView(UserAccessMixin, CreateView):
    """Create new transaction"""
    model = Transaction
    form_class = TransactionForm
    template_name = 'finance/transaction_form.html'
    success_url = reverse_lazy('transaction-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Transaction created successfully!')
        return super().form_valid(form)


class TransactionUpdateView(UserAccessMixin, UpdateView):
    """Update existing transaction"""
    model = Transaction
    form_class = TransactionForm
    template_name = 'finance/transaction_form.html'
    success_url = reverse_lazy('transaction-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Transaction updated successfully!')
        return super().form_valid(form)


class TransactionDeleteView(UserAccessMixin, DeleteView):
    """Delete transaction"""
    model = Transaction
    template_name = 'finance/transaction_confirm_delete.html'
    success_url = reverse_lazy('transaction-list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Transaction deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Category Views
class CategoryListView(UserAccessMixin, ListView):
    """List all user's categories"""
    model = Category
    template_name = 'finance/category_list.html'
    context_object_name = 'categories'


class CategoryCreateView(UserAccessMixin, CreateView):
    """Create new category"""
    model = Category
    form_class = CategoryForm
    template_name = 'finance/category_form.html'
    success_url = reverse_lazy('category-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Category created successfully!')
        return super().form_valid(form)


# Budget Views
class BudgetListView(UserAccessMixin, ListView):
    """List all user's budgets"""
    model = Budget
    template_name = 'finance/budget_list.html'
    context_object_name = 'budgets'


class BudgetCreateView(UserAccessMixin, CreateView):
    """Create new budget"""
    model = Budget
    form_class = BudgetForm
    template_name = 'finance/budget_form.html'
    success_url = reverse_lazy('budget-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Budget created successfully!')
        return super().form_valid(form)


@csrf_exempt
def health_check(request):
    """Health check endpoint for load balancers and monitoring systems."""
    try:
        # Check database connectivity
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        
        return HttpResponse(
            "OK - Finance Tracker is healthy",
            status=200,
            content_type="text/plain"
        )
    except Exception as e:
        return HttpResponse(
            f"ERROR - Database connection failed: {str(e)}",
            status=500,
            content_type="text/plain"
        )
