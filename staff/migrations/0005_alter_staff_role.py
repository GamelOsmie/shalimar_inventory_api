# Generated by Django 4.0.4 on 2022-05-30 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0004_alter_staff_designation_alter_staff_qualification_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='role',
            field=models.CharField(choices=[('Accountant', 'Accountant'), ('HR', 'HR'), ('Sales Executive', 'Sales Executive'), ('Credit Officer', 'Credit Officer')], max_length=50),
        ),
    ]
