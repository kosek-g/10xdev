from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Transaction, Category, Budget


class CustomUserCreationForm(UserCreationForm):
    """Custom user registration form with additional fields"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'username',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class CategoryForm(forms.ModelForm):
    """Form for creating and editing categories"""
    
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'description'
        )

    def clean_name(self):
        name = self.cleaned_data['name']
        if self.user:
            # Check for duplicate category names for this user
            existing = Category.objects.filter(user=self.user, name=name)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise forms.ValidationError('You already have a category with this name.')
        return name


class TransactionForm(forms.ModelForm):
    """Form for creating and editing transactions"""
    
    class Meta:
        model = Transaction
        fields = ['type', 'amount', 'date', 'category', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filter categories to show only user's categories
        if self.user:
            self.fields['category'].queryset = Category.objects.filter(user=self.user)
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('type', css_class='form-group col-md-6 mb-0'),
                Column('amount', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('date', css_class='form-group col-md-6 mb-0'),
                Column('category', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'description',
            Submit('submit', 'Save Transaction', css_class='btn btn-success')
        )


class BudgetForm(forms.ModelForm):
    """Form for creating and editing budgets"""
    
    class Meta:
        model = Budget
        fields = ['category', 'limit', 'period']
        widgets = {
            'limit': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filter categories to show only user's categories
        if self.user:
            self.fields['category'].queryset = Category.objects.filter(user=self.user)
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('category', css_class='form-group col-md-6 mb-0'),
                Column('period', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'limit'
        )

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        period = cleaned_data.get('period')
        
        if category and period and self.user:
            # Check for duplicate budget for same category and period
            existing = Budget.objects.filter(
                user=self.user, 
                category=category, 
                period=period
            )
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise forms.ValidationError(
                    f'You already have a {period.lower()} budget for {category.name}.'
                )
        
        return cleaned_data