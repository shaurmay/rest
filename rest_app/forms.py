from django.shortcuts import render, redirect, get_object_or_404
from .models import Dish, Category
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, OrderCreateForm # Твої форми з forms.py

# Форма реєстрації (ТЗ: Система автентифікації)
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '••••••••'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '••••••••'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш нікнейм'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.com'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("password_confirm"):
            raise forms.ValidationError("Паролі не збігаються!")
        return cleaned_data

# Форма оформлення замовлення (ТЗ: Оформлення замовлення)
class OrderCreateForm(forms.Form):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Іван Іванов'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+380...'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Вулиця, будинок, кв'}))
    comment = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}))
    
    PAYMENT_CHOICES = [
        ('cash', 'Готівка при отриманні'),
        ('online', 'Оплата онлайн'),
    ]
    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect())