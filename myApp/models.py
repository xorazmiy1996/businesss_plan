from django.db import models
from django.utils.text import slugify
from time import time
from django.shortcuts import reverse
from django.conf import settings

PROVINCE_CHOICES = [
    ("Andijon viloyati", "Andijon viloyati"),
    ("Buxoro viloyati", "Buxoro viloyati"),
    ("Fargʻona viloyati", "Fargʻona viloyati"),
    ("Jizzax viloyati", "Jizzax viloyati"),
    ("Xorazm viloyati", "Xorazm viloyati"),
    ("Namangan viloyati", "Namangan viloyati"),
    ("Navoiy viloyati", "Navoiy viloyati"),
    ("Qashqadaryo viloyati", "Qashqadaryo viloyati"),
    ("Qoraqalpogʻiston Respublikasi	", "Qoraqalpogʻiston Respublikasi"),
    ("Samarqand viloyati", "Sirdaryo viloyati"),
    ("Sirdaryo viloyati", "Sirdaryo viloyati"),
    ("Surxondaryo viloyati", "Surxondaryo viloyati"),
    ("Toshkent viloyati", "Toshkent viloyati"),

]

PLANNING_CHOICES = [
    ("BUSINESS_1", "BUSINESS_1"),
    ("BUSINESS_2", "BUSINESS_2"),
    ("BUSINESS_3", "BUSINESS_3"),
    ("BUSINESS GRANTS 1", "BUSINESS GRANTS 1"),
    ("BUSINESS GRANTS 2", "BUSINESS GRANTS 2"),

]

POSITION_CHOICES = [

    ("OPERATOR", "OPERATOR"),
    ("ENTREPRENEURS", "ENTREPRENEURS"),

]


class BaseModel(models.Model):
    # fields of the model
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# BusinessPlan
class BusinessPlanModel(BaseModel):

    # fields of the model
    image = models.ImageField()
    name_business = models.CharField(max_length=70)
    money_min = models.IntegerField()
    profit_year = models.IntegerField()
    profit_month = models.IntegerField()
    cost = models.IntegerField()
    text_min = models.TextField(max_length=100)

    def __str__(self):
        return self.name_business


# SystemUser
class SystemUserModel(BaseModel):
    # fields of the model
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="system_user")
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)

    def __str__(self):
        return self.user.full_name


# Order

class OrderModel(BaseModel):
    # fields of the model
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    province = models.CharField(max_length=50, choices=PROVINCE_CHOICES)
    region = models.CharField(max_length=50)
    additional_telephone = models.CharField(max_length=50)


    types_of_business = models.CharField(max_length=50, choices=PLANNING_CHOICES)
    order_id = models.ForeignKey(SystemUserModel, null=True, on_delete=models.CASCADE, related_name='orders')

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'


# Contact
class ContactModel(BaseModel):
    # fields of the model
    phone_number = models.CharField(max_length=15)
    order_information = models.OneToOneField(OrderModel, null=True, on_delete=models.CASCADE, related_name='contact')
    contact_id = models.ForeignKey(SystemUserModel, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.phone_number
