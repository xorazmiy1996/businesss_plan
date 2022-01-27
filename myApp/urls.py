from django.urls import path

# importing views from views.py
from .views import ContactAdd, BusinessPlanList, ContactList, OrderAdd

urlpatterns = [
    path('', BusinessPlanList.as_view(), name='business_plan_list_url'),

    path('contact/', ContactAdd.as_view(), name='contact_add_url'),
    path('contact_list/', ContactList.as_view(), name='contact_list_url'),

    path('order/', OrderAdd.as_view(), name='order_add_url'),

]
