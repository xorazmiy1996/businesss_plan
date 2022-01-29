from django.contrib import admin
from .models import Order, Phone, User, BusinessPlan

admin.site.register(BusinessPlan)
admin.site.register(Phone)
admin.site.register(Order)
admin.site.register(User)
