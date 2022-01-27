from django import forms
from .models import ContactModel, OrderModel


# USER FORMS model
class ContactForms(forms.ModelForm):
    class Meta:
        model = ContactModel
        fields = ['phone_number']

        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),

        }


class OrderForms(forms.ModelForm):
    class Meta:
        model = OrderModel
        fields = ['first_name', 'last_name', 'province', 'region', 'additional_telephone']
