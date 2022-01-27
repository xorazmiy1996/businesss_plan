from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from .models import ContactModel, BusinessPlanModel,OrderModel


class ContactAdd(CreateView):
    model = ContactModel
    template_name = 'myApp/contact_add.html'

    fields = ['phone_number']


class ContactList(ListView):
    model = ContactModel
    template_name = 'myApp/contact_list.html'


class OrderAdd(CreateView):
    model = OrderModel
    template_name = 'myApp/order_add.html'











class BusinessPlanList(ListView):
    model = BusinessPlanModel
    template_name = 'myApp/index.html'
