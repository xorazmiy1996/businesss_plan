from django.db import models
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save
from django.db.models import signals
from django.dispatch import receiver

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

BOOLEAN_CHOOSE = [
    ("100% to'langan", "100% to'langan"),
    ("50% to'langan", "50% to'langan"),
    ("25% to'langan", "25% to'langan"),
    ("to'lanmagan", "to'lanmagan"),
]


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User(AbstractUser, Base):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=100, choices=ROLE_CHOOSE)
    percentage = models.IntegerField(null=True, blank=True)

    objects = UserManager()

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        verbose_name = 'user1'
        verbose_name_plural = 'users1'

    def __str__(self):
        return self.get_username()


# Order

class Order(Base):
    phone_number = models.CharField(max_length=15)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    province = models.CharField(max_length=50, choices=PROVINCE_CHOICES, blank=True)
    region = models.CharField(max_length=50, blank=True)
    business_name = models.CharField(max_length=100, blank=True)
    business_type = models.CharField(max_length=50, choices=PLANNING_CHOICES, blank=True)
    payme = models.CharField(max_length=50, choices=BOOLEAN_CHOOSE, null=True, blank=True)

    # price = models.PositiveIntegerField()
    price = models.PositiveIntegerField(default=0)

    worker_field = models.ForeignKey(User, on_delete=models.CASCADE, related_name='worker_orders', blank=True,
                                     null=True)
    operator_field = models.ForeignKey(User, on_delete=models.CASCADE, related_name='operator_orders', blank=True,
                                       null=True)
    user_field = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_orders', blank=True, null=True)

    def __str__(self):
        return self.phone_number

    @property
    def operator_income(self):
        if self.payme:
            return int(self.price) * 0.15


# Phone
class Phone(Base):
    operator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='operator_name')
    number = models.CharField(max_length=15)

    def __str__(self):
        return self.number


class Petition(Base):
    working_phone = models.CharField(max_length=15, blank=True)
    viewed = models.BooleanField(null=True)

    def __str__(self):
        return self.working_phone


@receiver(signals.post_save, sender=Petition)
def order_create(sender, instance, **kwargs):
    phone_number = Order.objects.create(phone_number=Petition.objects.last())
    instance.phone_number = phone_number
