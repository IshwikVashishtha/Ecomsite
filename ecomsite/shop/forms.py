from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Review

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Full Name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email Address'
    }))
    phone = forms.CharField(max_length=15, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Phone Number'
    }))
    address = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 3,
        'placeholder': 'Delivery Address'
    }))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'City'
    }))
    state = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'State'
    }))
    zipcode = forms.CharField(max_length=10, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'ZIP Code'
    }))

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)], attrs={
                'class': 'form-control'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your review...'
            })
        }

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Search products...'
    }))
    category = forms.ChoiceField(choices=[], required=False, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    min_price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Min Price'
    }))
    max_price = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Max Price'
    }))
    sort_by = forms.ChoiceField(choices=[
        ('', 'Sort by'),
        ('price_low', 'Price: Low to High'),
        ('price_high', 'Price: High to Low'),
        ('newest', 'Newest First'),
        ('rating', 'Highest Rated'),
    ], required=False, widget=forms.Select(attrs={
        'class': 'form-control'
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Category
        categories = Category.objects.all()
        self.fields['category'].choices = [('', 'All Categories')] + [(cat.id, cat.name) for cat in categories]
