# Generated by Django 4.0.4 on 2022-05-22 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('Super Admin', 'Super Admin'), ('Admin', 'Admin'), ('Import Officer', 'Import Officer'), ('Tracking Officer', 'Tracking Officer'), ('Warehouse Officer', 'Warehouse Officer'), ('Branch Officer', 'Branch Officer'), ('Service Station Officer', 'Service Station Officer'), ('Website Manager', 'Website Manager')], default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='workplace',
            field=models.CharField(blank=True, default='General', max_length=50, null=True),
        ),
    ]
