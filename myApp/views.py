from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Contact, BusinessPlan, Order


# Contact CRUD
class ContactAdd(CreateView):
    model = Contact
    template_name = 'myApp/contact_add.html'

    fields = ['phone_number']


class ContactList(ListView):
    model = Contact
    template_name = 'myApp/contact_list.html'


class ContactDetailsView(DetailView):
    model = Contact
    template_name = 'myApp/contact_detail.html'


# Order CRUD
class OrderAdd(CreateView):
    model = Order
    template_name = 'myApp/order_add.html'
    fields = '__all__'


class OrderList(ListView):
    model = Order
    template_name = 'myApp/order_list.html'


class OrderDetailView(DetailView):
    model = Order
    template_name = 'myApp/order_detail.html'


# Business Plan List
class BusinessPlanList(ListView):
    model = BusinessPlan
    template_name = 'myApp/index.html'


class BusinessPlanAdd(CreateView):
    model = BusinessPlan
    template_name = 'myApp/business_plan_add.html'
    fields = '__all__'







