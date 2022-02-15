from django.contrib import admin
from .models import Order, Phone, User, Petition, GrantProject

# admin.site.register(BusinessPlan)
admin.site.register(Petition)
admin.site.register(Phone)
admin.site.register(Order)
admin.site.register(User)
admin.site.register(GrantProject)
