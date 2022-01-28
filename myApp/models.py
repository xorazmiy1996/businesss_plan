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
    # fields of the model
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# SystemUser
class User(Base, AbstractUser):
    # fields of the model
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(choices=ROLE_CHOOSE)
    percentage = models.IntegerField()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.first_name


# Order

class Order(Base):
    province = models.CharField(max_length=50, choices=PROVINCE_CHOICES)
    region = models.CharField(max_length=50)
    business_name = models.CharField(max_length=50)
    business_type = models.CharField(max_length=50, choices=PLANNING_CHOICES)
    price = models.IntegerField()

    worker = models.ForeignKey(User, on_delete=models.CASCADE, releted_name='worker')
    operator = models.ForeignKey(User, on_delete=models.CASCADE, releted_name='operator')
    user = models.ForeignKey(User, on_delete=models.CASCADE, releted_name='user')

    def __str__(self):
        return self.price


# Phone
class Phone(Base):
    phone = models.ForeignKey(User, on_delete=models.CASCADE, related_name='phone')
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
    name_business = models.CharField(max_length=70)
    money_min = models.IntegerField()
    profit_year = models.IntegerField()
    profit_month = models.IntegerField()
    cost = models.IntegerField()
    text_min = models.TextField(max_length=100)

    def __str__(self):
        return self.name_business
