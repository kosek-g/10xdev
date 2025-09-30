from django.urls import path
from . import views

urlpatterns = [
    # Health check
    path('health/', views.health_check, name='health-check'),
    
    # Dashboard
    path('', views.dashboard_view, name='dashboard'),
    
    # Authentication
    path('register/', views.register_view, name='register'),
    
    # Transactions
    path('transactions/', views.TransactionListView.as_view(), name='transaction-list'),
    path('transactions/create/', views.TransactionCreateView.as_view(), name='transaction-create'),
    path('transactions/<int:pk>/edit/', views.TransactionUpdateView.as_view(), name='transaction-edit'),
    path('transactions/<int:pk>/delete/', views.TransactionDeleteView.as_view(), name='transaction-delete'),
    
    # Categories
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category-create'),
    
    # Budgets
    path('budgets/', views.BudgetListView.as_view(), name='budget-list'),
    path('budgets/create/', views.BudgetCreateView.as_view(), name='budget-create'),
]