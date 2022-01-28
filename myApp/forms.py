from django import forms
from .models import Contact, Order


# USER FORMS model
class ContactForms(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['phone_number']

        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),

        }


class OrderForms(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'province', 'region', 'additional_telephone', 'types_of_business']
