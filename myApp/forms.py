from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

COLOR_CHOOSE = [
    ('green', " green"),
    ('yellow', "yellow"),
    ('red', "red"),
]


class AdminUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'phone_user', 'add_phone_user']


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

        fields = ['add_phone_number', 'first_name', 'last_name', 'province', 'region', 'business_name',
                  'business_type', 'quality',
                  'price', 'stat_date', 'end_date', 'payme', 'color_type', 'document']

        # widgets = {
        #
        #     'add_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        #     'first_name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'province': forms.Select(attrs={'class': 'form-select'}),
        #     'region': forms.Select(attrs={'class': 'form-select'}),
        #
        #     'business_name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'business_type': forms.Select(attrs={'class': 'form-select'}),
        #     'quality': forms.Select(attrs={'class': 'form-select'}),
        #     'price': forms.TextInput(attrs={'class': 'form-control'}),
        #
        #
        #     'stat_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        #     'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        #     'payme': forms.TextInput(attrs={'class': 'form-control'}),
        #     'color_type': forms.RadioSelect(choices=COLOR_CHOOSE),
        #
        # }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['region'].queryset = Region.objects.none()

            if 'province' in self.data:
                try:
                    province_id = int(self.data.get('province'))
                    self.fields['region'].queryset = Region.objects.filter(province_id=province_id).order_by('name')
                except (ValueError, TypeError):
                    pass  # invalid input from the client; ignore and fallback to empty City queryset
            elif self.instance.pk:
                self.fields['region'].queryset = self.instance.province.region_set.order_by('name')


class PreOrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['phone_number', 'add_phone_number', 'first_name', 'last_name', 'province', 'region', 'comment',
                  'business_name',
                  'business_type',
                  'price', 'stat_date', 'end_date', 'payme', 'color_type']


class IndividualOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['phone_number', 'add_phone_number', 'first_name', 'last_name', 'province', 'region', 'business_name',
                  'business_type', 'quality',
                  'price', 'stat_date', 'end_date', 'payme', 'color_type', 'document']



        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['region'].queryset = Region.objects.none()

            if 'province' in self.data:
                try:
                    province_id = int(self.data.get('province'))
                    self.fields['region'].queryset = Region.objects.filter(province_id=province_id).order_by('name')
                except (ValueError, TypeError):
                    pass  # invalid input from the client; ignore and fallback to empty City queryset
            elif self.instance.pk:
                self.fields['region'].queryset = self.instance.province.region_set.order_by('name')


class WorkerOrderUpdate(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['add_phone_number', 'first_name', 'last_name', 'province', 'region', 'business_name', 'business_type',
                  'price', 'payme',
                  'status']

        widgets = {
            'add_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'province': forms.Select(attrs={'class': 'form-select'}),

            'region': forms.Select(attrs={'class': 'form-select'}),

            'business_name': forms.TextInput(attrs={'class': 'form-control'}),
            'business_type': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'payme': forms.Select(attrs={'class': 'form-select'}),
            # 'status': forms.BooleanField(),

        }


class GrantForm(forms.ModelForm):
    class Meta:
        model = GrantProject
        fields = ['organization', 'project_name', 'price', 'end_time', 'link']

        widgets = {
            'organization': forms.TextInput(attrs={'class': 'form-control'}),
            'project_name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'link': forms.TextInput(attrs={'class': 'form-control'}),

        }


class BusinessForm(forms.ModelForm):
    class Meta:
        model = BusinessPlan
        fields = ['image', 'name_business', 'money_min', 'profit_year', 'profit_month', 'number_of_workers',
                  'land_area', 'cost', 'answer', 'text_min']

        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'name_business': forms.TextInput(attrs={'class': 'form-control'}),
            'money_min': forms.TextInput(attrs={'class': 'form-control'}),
            'profit_year': forms.TextInput(attrs={'class': 'form-control'}),
            'profit_month': forms.TextInput(attrs={'class': 'form-control'}),
            'number_of_workers': forms.TextInput(attrs={'class': 'form-control'}),
            'land_area': forms.TextInput(attrs={'class': 'form-control'}),
            'answer': forms.TextInput(attrs={'class': 'form-control'}),
            'cost': forms.TextInput(attrs={'class': 'form-control'}),
            'text_min': forms.Textarea(attrs={'class': 'form-control'}),

        }


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['image', 'first_name', 'last_name', 'middle_name', 'academic_degree', 'text_min']

        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'academic_degree': forms.TextInput(attrs={'class': 'form-control'}),
            'text_min': forms.Textarea(attrs={'class': 'form-control'}),

        }


class GrantForm(forms.ModelForm):
    class Meta:
        model = GrantProject
        fields = [
            "category",
            "organization",
            "project_name",
            "price",
            "end_time",
            "link",

        ]

        widgets = {

            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'organization': forms.TextInput(attrs={'class': 'form-control'}),
            'project_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'link': forms.TextInput(attrs={'class': 'form-control'}),

        }

class MyOrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order

        fields = ['add_phone_number', 'first_name', 'last_name', 'province', 'region', 'business_name',
                  'business_type', 'quality',
                  'price', 'payme',  'document']


        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['region'].queryset = Region.objects.none()

            if 'province' in self.data:
                try:
                    province_id = int(self.data.get('province'))
                    self.fields['region'].queryset = Region.objects.filter(province_id=province_id).order_by('name')
                except (ValueError, TypeError):
                    pass  # invalid input from the client; ignore and fallback to empty City queryset
            elif self.instance.pk:
                self.fields['region'].queryset = self.instance.province.region_set.order_by('name')