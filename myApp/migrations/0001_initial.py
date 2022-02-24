# Generated by Django 4.0.1 on 2022-02-23 08:09

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
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
            name='User',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='myApp.base')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('role', models.CharField(choices=[('admin', 'admin'), ('Operator', 'Operator'), ('Worker', 'Worker'), ('user', 'user')], max_length=100)),
                ('percentage', models.IntegerField(blank=True, null=True)),
                ('number_of_orders', models.IntegerField(default=3, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
                'swappable': 'AUTH_USER_MODEL',
            },
            bases=('myApp.base', models.Model),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='BusinessPlan',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='myApp.base')),
                ('image', models.ImageField(null=True, upload_to='images/')),
                ('name_business', models.CharField(max_length=100)),
                ('money_min', models.IntegerField()),
                ('profit_year', models.IntegerField()),
                ('profit_month', models.IntegerField()),
                ('cost', models.IntegerField()),
                ('text_min', models.TextField(max_length=100)),
            ],
            bases=('myApp.base',),
        ),
        migrations.CreateModel(
            name='GrantProject',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='myApp.base')),
                ('organization', models.CharField(max_length=150)),
                ('project_name', models.CharField(max_length=150)),
                ('price', models.IntegerField(default=0)),
                ('end_time', models.DateTimeField()),
                ('link', models.CharField(max_length=256)),
            ],
            bases=('myApp.base',),
        ),
        migrations.CreateModel(
            name='Petition',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='myApp.base')),
                ('working_phone', models.CharField(blank=True, max_length=15)),
                ('viewed', models.BooleanField(null=True)),
            ],
            bases=('myApp.base',),
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='myApp.base')),
                ('number', models.CharField(max_length=15)),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operator_name', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('myApp.base',),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='myApp.base')),
                ('phone_number', models.CharField(max_length=15)),
                ('first_name', models.CharField(blank=True, max_length=50)),
                ('last_name', models.CharField(blank=True, max_length=50)),
                ('province', models.CharField(blank=True, choices=[('Andijon viloyati', 'Andijon viloyati'), ('Buxoro viloyati', 'Buxoro viloyati'), ('Fargʻona viloyati', 'Fargʻona viloyati'), ('Jizzax viloyati', 'Jizzax viloyati'), ('Xorazm viloyati', 'Xorazm viloyati'), ('Namangan viloyati', 'Namangan viloyati'), ('Navoiy viloyati', 'Navoiy viloyati'), ('Qashqadaryo viloyati', 'Qashqadaryo viloyati'), ('Qoraqalpogʻiston Respublikasi\t', 'Qoraqalpogʻiston Respublikasi'), ('Samarqand viloyati', 'Sirdaryo viloyati'), ('Sirdaryo viloyati', 'Sirdaryo viloyati'), ('Surxondaryo viloyati', 'Surxondaryo viloyati'), ('Toshkent viloyati', 'Toshkent viloyati')], max_length=50)),
                ('region', models.CharField(blank=True, max_length=50)),
                ('business_name', models.CharField(blank=True, max_length=100)),
                ('business_type', models.CharField(blank=True, choices=[('business', 'Biznes Reja'), ('teo', 'TEO'), ('grand', 'Grand'), ('boshqa', 'Boshqa')], max_length=50)),
                ('payme', models.CharField(blank=True, choices=[("100% to'langan", "100% to'langan"), ("75% to'langan", "75% to'langan"), ("50% to'langan", "50% to'langan"), ("25% to'langan", "25% to'langan"), ("to'lanmagan", "to'lanmagan"), ("qiziqish yo'q", "qiziqish yo'q")], max_length=50, null=True)),
                ('price', models.PositiveIntegerField(default=0)),
                ('status', models.BooleanField(default=False)),
                ('operator_field', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='operator_orders', to=settings.AUTH_USER_MODEL)),
                ('user_field', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_orders', to=settings.AUTH_USER_MODEL)),
                ('worker_field', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='worker_orders', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('myApp.base',),
        ),
    ]