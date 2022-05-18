# Generated by Django 4.0.4 on 2022-05-17 17:36

import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.functions.text
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('slug', models.SlugField(blank=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=40, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=40, null=True)),
                ('last_name', models.CharField(blank=True, max_length=40, null=True)),
                ('role', models.CharField(blank=True, choices=[('Super Admin', 'Super Admin'), ('Admin', 'Admin'), ('Import Officer', 'Import Officer'), ('Tracking Officer', 'Tracking Officer'), ('Warehouse Officer', 'Warehouse Officer'), ('Branch Officer', 'Branch Officer'), ('Service Station Officer', 'Service Station Officer'), ('Website Manager', 'Website Manager')], default=None, max_length=50, null=True)),
                ('workplace', models.CharField(blank=True, default='General', max_length=50, null=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_superadmin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_verified', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': [django.db.models.functions.text.Lower('first_name')],
            },
        ),
    ]
