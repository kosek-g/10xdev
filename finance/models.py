from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class Category(models.Model):
    """Model for expense and income categories - user specific"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100, unique=False)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        unique_together = ('user', 'name')
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.user.username})"


class Transaction(models.Model):
    """Model for financial transactions"""
    TRANSACTION_TYPES = [
        ('Income', 'Income'),
        ('Expense', 'Expense'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='transactions')
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.type}: {self.amount} - {self.description} ({self.user.username})"


class Budget(models.Model):
    """Model for budget limits per category"""
    PERIOD_CHOICES = [
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
        ('Quarterly', 'Quarterly'),
        ('Yearly', 'Yearly'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='budgets')
    limit = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES, default='Monthly')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'category', 'period')
        ordering = ['category__name']
    
    def __str__(self):
        return f"{self.category.name} - {self.limit} ({self.period}) - {self.user.username}"
    
    def get_spending_percentage(self, start_date, end_date):
        """Calculate spending percentage for this budget in given period"""
        total_spent = self.category.transactions.filter(
            user=self.user,
            type='Expense',
            date__range=[start_date, end_date]
        ).aggregate(
            total=models.Sum('amount')
        )['total'] or Decimal('0.00')
        
        if self.limit > 0:
            return min((total_spent / self.limit) * 100, 100)
        return 0
