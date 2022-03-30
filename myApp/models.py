from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save
from django.db.models import signals, Q
from django.dispatch import receiver

from datetime import datetime

from django.db.models import Sum

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
    ("admin", "boss"),
    ("Operator", "ishchi-xodim"),

]

PLANNING_CHOICES = [
    ("business", "Biznes Reja"),
    ("teo", "TEO"),
    ("grand", "Grand"),
    ("boshqa", "Boshqa"),
    ("qiziqmadi", "Qiziqish bo'lmadi"),

]

POSITION_CHOICES = [

    ("OPERATOR", "OPERATOR"),
    ("ENTREPRENEURS", "ENTREPRENEURS"),

]

QUALITY_CHOICES = [

    ("narx", "Narx"),
    ("sifat", "Sifat"),
    ("narx+sifat", "Narx + Sifat"),

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


class Province(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Region(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User(AbstractUser, Base):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=100, choices=ROLE_CHOOSE)
    percentage = models.IntegerField(null=True, blank=True)
    # number_of_orders = models.IntegerField(null=True, default=3)
    phone_user = models.CharField(max_length=17)
    add_phone_user = models.CharField(max_length=17)

    objects = UserManager()

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.get_username()

    def get_absolute_url(self):
        return reverse('user_detail_url', kwargs={'pk': self.pk})

    @property
    def all_profit(self, *args):
        return Order.objects.filter(Q(worker_field=self) | Q(operator_field=self)).filter(price__isnull=False)
        # .aggregate(
        #     sum_price=Sum('price')
        # )['sum_price']

    @property
    def all_orders(self):
        return Order.objects.filter(Q(worker_field=self) | Q(operator_field=self))

    @property
    def order_count(self):
        return self.worker_orders.filter(status='False')

    #
    # @property
    # def worker_order_count(self):
    #     return self.worker_orders.filter(status='False')

    @property
    def orders(self):
        return Order.objects.filter(Q(worker_field=self) | Q(operator_field=self))

    @property
    def grant_count(self):  # worker_field_id=self.id  <=> worker_field=self
        return Order.objects.filter(Q(worker_field=self) | Q(operator_field=self)).filter(business_type='grand')

    @property
    def business_count(self):
        return Order.objects.filter(Q(worker_field=self) | Q(operator_field=self)).filter(
            business_type='business')

    @property
    def teo_count(self):
        return Order.objects.filter(Q(worker_field=self) | Q(operator_field=self)).filter(business_type='teo')

    @property
    def boshqa_count(self):
        return Order.objects.filter(Q(worker_field=self) | Q(operator_field=self)).filter(
            business_type='boshqa')

    # yangilari
    @property
    def unpaid(self):
        return Order.objects.filter(Q(operator_field=self)).filter(payme__exact="to'lanmagan")

    @property
    def payme25(self):
        return Order.objects.filter(Q(operator_field=self)).filter(payme__exact="25% to'langan")

    @property
    def payme50(self):
        return Order.objects.filter(Q(operator_field=self)).filter(payme__exact="50% to'langan")

    @property
    def payme75(self):
        return Order.objects.filter(Q(operator_field=self)).filter(payme__exact="75% to'langan")

    @property
    def payme100(self):
        return Order.objects.filter(Q(operator_field=self)).filter(payme__exact="100% to'langan")

    @property
    def grant_list(self):
        return Order.objects.filter(Q(operator_field=self)).filter(business_type__exact="grand")

    @property
    def teo_list(self):
        return Order.objects.filter(Q(operator_field=self)).filter(business_type__exact="teo")

    @property
    def business_list(self):
        return Order.objects.filter(Q(operator_field=self)).filter(business_type__exact="business")

    @property
    def boshqa_list(self):
        return Order.objects.filter(Q(operator_field=self)).filter(business_type__exact="boshqa")

    #
    # def price(self):
    #     summ = 0
    #     for order in self.orders.all():
    #         summ += int(order.price)
    #     return summ


# Order

class Order(Base):
    phone_number = models.CharField(max_length=15)
    add_phone_number = models.CharField(max_length=15, blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, blank=True, null=True)
    business_name = models.CharField(max_length=100, blank=True)
    business_type = models.CharField(max_length=50, choices=PLANNING_CHOICES, blank=True)

    quality = models.CharField(max_length=50, choices=QUALITY_CHOICES, blank=True)
    price = models.PositiveIntegerField(default=0)
    payme = models.CharField(max_length=50, null=True, blank=True)

    order_finished_date = models.DateTimeField(default=None, blank=True, null=True)

    # color_type = models.CharField(max_length=15, null=True, blank=True)
    color_type = models.CharField(max_length=15, blank=True, null=True)

    petition_type = models.CharField(max_length=20, blank=True, null=True)

    stat_date = models.DateTimeField(verbose_name='Start', default=None, blank=True, null=True)

    end_date = models.DateTimeField(default=None, blank=True, null=True)

    status = models.BooleanField(default=False, verbose_name='Ish tugallandimi:')

    worker_field = models.ForeignKey(User, on_delete=models.CASCADE, related_name='worker_orders', blank=True,
                                     null=True)
    operator_field = models.ForeignKey(User, on_delete=models.CASCADE, related_name='operator_orders', blank=True,
                                       null=True)
    user_field = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_orders', blank=True, null=True)

    class Meta:
        ordering = ('updated_at',)

    def __str__(self):
        return self.phone_number

    def get_absolute_url(self):
        return reverse('order_detail_url', kwargs={'pk': self.pk})

    # @property
    # def get_status_color(self):
    #     middle = (self.end_date.timestamp() - self.stat_date.timestamp()) / 3
    #     first_interval = self.stat_date.timestamp() + middle
    #     second_interval = self.end_date.timestamp() - middle
    #     current_time = datetime.now().timestamp()
    #
    #     if current_time < first_interval:
    #         return "green"
    #     elif current_time >= first_interval and current_time < second_interval:
    #         return "yellow"
    #     else:
    #         return "red"



    # @property
    # def get_timestamp_start_date(self):
    #     return self.stat_date.strftime("%d/%m/%y %H:%M:%S")
    # @property
    # def get_timestamp_end_date(self):
    #     return self.end_date.strftime("%d/%m/%y %H:%M:%S")

    @property
    def get_timestamp_start_date(self):
        if self.stat_date not in [None, '']:
            return self.stat_date.strftime("%d/%m/%y %H:%M:%S")
        else:
            return '0'

    @property
    def get_timestamp_end_date(self):
        if self.stat_date not in [None, '']:
            return self.end_date.strftime("%d/%m/%y %H:%M:%S")
        else:
            return '0'





    # @property
    # def order_count(self):
    #     return Order.objects.all().count()

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
    # working_phone = models.CharField(max_length=15, verbose_name='Telefon:')

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Telefon raqami quyidagi formatda kiritilishi kerak: +99 893 090 10 07.")
    working_phone = models.CharField(validators=[phone_regex], max_length=17, blank=True, verbose_name='Telefon:')

    viewed = models.BooleanField(null=True)

    def __str__(self):
        return self.working_phone


@receiver(signals.post_save, sender=Petition)
def order_create(sender, instance, **kwargs):
    phone_number = Order.objects.create(phone_number=Petition.objects.last())


class GrantProject(Base):
    category = models.CharField(max_length=70, blank=True, null=True)
    organization = models.CharField(max_length=150)
    project_name = models.CharField(max_length=150)
    price = models.CharField(max_length=30, default=0)
    end_time = models.DateTimeField(verbose_name='Deadline')
    link = models.CharField(max_length=256)

    def __str__(self):
        return self.project_name


class BusinessPlan(Base):
    # fields of the model
    image = models.ImageField(null=True, upload_to='images/')
    name_business = models.CharField(max_length=100)
    money_min = models.CharField(max_length=70)
    profit_year = models.CharField(max_length=70)
    profit_month = models.CharField(max_length=70)
    cost = models.IntegerField()
    text_min = models.TextField(max_length=100)

    # o'zgarish
    number_of_workers = models.CharField(max_length=70)
    land_area = models.CharField(max_length=70)
    answer = models.CharField(max_length=70)

    def __str__(self):
        return self.name_business


class Team(Base):
    image = models.ImageField(null=True, upload_to='images/')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    academic_degree = models.CharField(max_length=60)
    text_min = models.TextField(max_length=150)
