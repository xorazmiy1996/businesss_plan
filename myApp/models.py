from django.db import models
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save
from django.db.models import signals, Q
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
    ("business", "Biznes Reja"),
    ("teo", "TEO"),
    ("grand", "Grand"),
    ("boshqa", "Boshqa"),

]

POSITION_CHOICES = [

    ("OPERATOR", "OPERATOR"),
    ("ENTREPRENEURS", "ENTREPRENEURS"),

]

BOOLEAN_CHOOSE = [
    ("100% to'langan", "100% to'langan"),
    ("75% to'langan", "75% to'langan"),
    ("50% to'langan", "50% to'langan"),
    ("25% to'langan", "25% to'langan"),
    ("to'lanmagan", "to'lanmagan"),
    ("qiziqish yo'q", "qiziqish yo'q"),
]

STATUS_CHOOSE = [
    ('bajarilmoqda', "Bajarilmoqda"),
    ('bajarildi', "Bajarildi"),
]


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User(AbstractUser, Base):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=100, choices=ROLE_CHOOSE)
    percentage = models.IntegerField(null=True, blank=True)
    number_of_orders = models.IntegerField(null=True,default=3)

    objects = UserManager()

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.get_username()

    def order_count(self):
        return self.worker_orders.filter(status='False').count()

    @property
    def grant_count(self):  # worker_field_id=self.id  <=> worker_field=self
        return Order.objects.filter(Q(worker_field=self) | Q(operator_field=self)).filter(business_type='grand').count()

    @property
    def business_count(self):
        return Order.objects.filter(Q(worker_field=self) | Q(operator_field=self)).filter(
            business_type='business').count()

    @property
    def teo_count(self):
        return Order.objects.filter(Q(worker_field=self) | Q(operator_field=self)).filter(business_type='teo').count()

    @property
    def boshqa_count(self):
        return Order.objects.filter(Q(worker_field=self) | Q(operator_field=self)).filter(
            business_type='boshqa').count()


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

    status = models.BooleanField(default=False)

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


class GrantProject(Base):
    organization = models.CharField(max_length=150)
    project_name = models.CharField(max_length=150)
    price = models.IntegerField(default=0)
    end_time = models.DateTimeField()
    link = models.CharField(max_length=256)

    def __str__(self):
        return self.project_name


class BusinessPlan(Base):
    # fields of the model
    image = models.ImageField(null=True, upload_to='images/')
    name_business = models.CharField(max_length=100)
    money_min = models.IntegerField()
    profit_year = models.IntegerField()
    profit_month = models.IntegerField()
    cost = models.IntegerField()
    text_min = models.TextField(max_length=100)

    def __str__(self):
        return self.name_business
