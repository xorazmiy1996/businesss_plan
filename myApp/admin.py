from django.contrib import admin
from .models import OrderModel, ContactModel, SystemUserModel, BusinessPlanModel

admin.site.register(BusinessPlanModel)
admin.site.register(ContactModel)
admin.site.register(OrderModel)
admin.site.register(SystemUserModel)
