from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm


class AdminUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role']


# class UserCreateForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email', 'role']


# USER FORMS model
class PetitionForm(forms.ModelForm):
    class Meta:
        model = Petition
        fields = ['working_phone']

        widgets = {
            'working_phone': forms.TextInput(attrs={'class': 'form-control'}),

        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'province', 'region', 'business_name', 'business_type', 'price', 'payme']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'province': forms.Select(attrs={'class': 'form-select'}),
            'region': forms.TextInput(attrs={'class': 'form-control'}),

            'business_name': forms.TextInput(attrs={'class': 'form-control'}),
            'business_type': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'payme': forms.Select(attrs={'class': 'form-select'}),

        }


class GrantForm(forms.ModelForm):
    class Meta:
        model = GrantProject
        fields = ['organization', 'project_name', 'price', 'end_time', 'link']

        widgets = {
            'organization': forms.TextInput(attrs={'class': 'form-control'}),
            'project_name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control','type': 'datetime-local'}),
            'link': forms.TextInput(attrs={'class': 'form-control'}),

        }
