from .models import Dish, Client
from django import forms

# Форма реєстрації (ТЗ: Система автентифікації)
# class RegistrationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '••••••••'}))
#     password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '••••••••'}))

#     class Meta:
#         model = Client
#         fields = ['username', 'email', 'password']
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваш нікнейм'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.com'}),
#         }

#     def clean(self):
#         cleaned_data = super().clean()
#         if cleaned_data.get("password") != cleaned_data.get("password_confirm"):
#             raise forms.ValidationError("Паролі не збігаються!")
#         return cleaned_data

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


class ClientCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторіть пароль'}))

    class Meta:
        model = Client
        fields = ("username", "email")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ваш нікнейм"}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.com'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Паролі не збігаються")
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        # store raw password (for this simple project). For production, hash it.
        instance.password = self.cleaned_data.get('password1')
        if commit:
            instance.save()
        return instance

class ClientUpdateForm(forms.ModelForm):
    class Meta:
        model = Client
        # Client model doesn't have a separate 'name' field (it uses AbstractUser fields).
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

