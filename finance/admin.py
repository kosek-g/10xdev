from django.contrib import admin
from .models import Category, Transaction, Budget


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for Category model"""
    list_display = ['name', 'user', 'created_at']
    list_filter = ['user', 'created_at']
    search_fields = ['name', 'description', 'user__username']
    ordering = ['user', 'name']
    
    def get_queryset(self, request):
        """Filter categories to show only current user's or all for superusers"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Admin interface for Transaction model"""
    list_display = ['description', 'type', 'amount', 'date', 'category', 'user', 'created_at']
    list_filter = ['type', 'category', 'user', 'date', 'created_at']
    search_fields = ['description', 'user__username', 'category__name']
    ordering = ['-date', '-created_at']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Transaction Details', {
            'fields': ('user', 'type', 'amount', 'date', 'category', 'description')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        """Filter transactions to show only current user's or all for superusers"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Filter category choices to show only user's categories"""
        if db_field.name == "category" and not request.user.is_superuser:
            kwargs["queryset"] = Category.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    """Admin interface for Budget model"""
    list_display = ['category', 'limit', 'period', 'user', 'created_at']
    list_filter = ['period', 'user', 'category', 'created_at']
    search_fields = ['category__name', 'user__username']
    ordering = ['user', 'category__name']
    
    def get_queryset(self, request):
        """Filter budgets to show only current user's or all for superusers"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Filter category choices to show only user's categories"""
        if db_field.name == "category" and not request.user.is_superuser:
            kwargs["queryset"] = Category.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# Customize admin site header and title
admin.site.site_header = "Finance Tracker Administration"
admin.site.site_title = "Finance Tracker Admin"
admin.site.index_title = "Welcome to Finance Tracker Administration"
