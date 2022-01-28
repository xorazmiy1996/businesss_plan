# Generated by Django 4.0.1 on 2022-01-27 12:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Base',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='BusinessPlan',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='myApp.base')),
                ('image', models.ImageField(upload_to='')),
                ('name_business', models.CharField(max_length=70)),
                ('money_min', models.IntegerField()),
                ('profit_year', models.IntegerField()),
                ('profit_month', models.IntegerField()),
                ('cost', models.IntegerField()),
                ('text_min', models.TextField(max_length=100)),
            ],
            bases=('myApp.base',),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='myApp.base')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('province', models.CharField(choices=[('Andijon viloyati', 'Andijon viloyati'), ('Buxoro viloyati', 'Buxoro viloyati'), ('Fargʻona viloyati', 'Fargʻona viloyati'), ('Jizzax viloyati', 'Jizzax viloyati'), ('Xorazm viloyati', 'Xorazm viloyati'), ('Namangan viloyati', 'Namangan viloyati'), ('Navoiy viloyati', 'Navoiy viloyati'), ('Qashqadaryo viloyati', 'Qashqadaryo viloyati'), ('Qoraqalpogʻiston Respublikasi\t', 'Qoraqalpogʻiston Respublikasi'), ('Samarqand viloyati', 'Sirdaryo viloyati'), ('Sirdaryo viloyati', 'Sirdaryo viloyati'), ('Surxondaryo viloyati', 'Surxondaryo viloyati'), ('Toshkent viloyati', 'Toshkent viloyati')], max_length=50)),
                ('region', models.CharField(max_length=50)),
                ('additional_telephone', models.CharField(max_length=50)),
                ('types_of_business', models.CharField(choices=[('BUSINESS_1', 'BUSINESS_1'), ('BUSINESS_2', 'BUSINESS_2'), ('BUSINESS_3', 'BUSINESS_3'), ('BUSINESS GRANTS 1', 'BUSINESS GRANTS 1'), ('BUSINESS GRANTS 2', 'BUSINESS GRANTS 2')], max_length=50)),
            ],
            bases=('myApp.base',),
        ),
        migrations.CreateModel(
            name='SystemUser',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='myApp.base')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='system_user', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('myApp.base',),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='myApp.base')),
                ('phone_number', models.CharField(max_length=15)),
                ('order_information', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contact', to='myApp.order')),
            ],
            bases=('myApp.base',),
        ),
    ]
