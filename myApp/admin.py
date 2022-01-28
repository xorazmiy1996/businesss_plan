from django.contrib import admin
from .models import Order, Contact, User, BusinessPlan

admin.site.register(BusinessPlan)
admin.site.register(Contact)
admin.site.register(Order)
admin.site.register(User)
