from django.urls import path

# importing views from views.py
from .views import *

urlpatterns = [
    path('', BusinessPlanList.as_view(), name='home_url'),
    path('business/', BusinessPlanAdd.as_view(), name='business_plan_add_url'),

]
