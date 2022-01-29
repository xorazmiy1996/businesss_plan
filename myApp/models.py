from django.db import models
from django.utils.text import slugify
from time import time
from django.shortcuts import reverse
from django.conf import settings
from django.contrib.auth.models import AbstractUser

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

ROLE_CHOOSE = [
    ("admin", "admin"),
    ("Operator", "Operator"),
    ("Worker", "Worker"),
    ("user", "user"),

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


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User(AbstractUser, Base):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=100,choices=ROLE_CHOOSE)
    percentage = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.get_username()


# Order

class Order(Base):
    province = models.CharField(max_length=50, choices=PROVINCE_CHOICES)
    region = models.CharField(max_length=50)
    business_name = models.CharField(max_length=100)
    business_type = models.CharField(max_length=50, choices=PLANNING_CHOICES)
    price = models.IntegerField()

    worker_field = models.ForeignKey(User, on_delete=models.CASCADE, related_name='worker_orders')
    operator_field = models.ForeignKey(User, on_delete=models.CASCADE, related_name='operator_orders')
    user_field = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_orders')

    def __str__(self):
        return self.business_name


# Phone
class Phone(Base):
    operator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='operator_name')
    number = models.CharField(max_length=15)

    def __str__(self):
        return self.number


class Application(Base):
    working_phone = models.CharField(max_length=15)
    viewed = models.BooleanField()


# BusinessPlan
class BusinessPlan(Base):
    # fields of the model
    image = models.ImageField()
    name_business = models.CharField(max_length=100)
    money_min = models.IntegerField()
    profit_year = models.IntegerField()
    profit_month = models.IntegerField()
    cost = models.IntegerField()
    text_min = models.TextField(max_length=100)

    def __str__(self):
        return self.name_business
