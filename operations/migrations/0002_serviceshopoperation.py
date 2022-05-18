# Generated by Django 4.0.4 on 2022-05-17 23:53

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.functions.text
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0001_initial'),
        ('units', '0002_serviceshop'),
        ('operations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceShopOperation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('service_shop', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='service_shops', to='units.serviceshop')),
                ('spare_parts_damaged', models.ManyToManyField(blank=True, related_name='service_shop_spare_parts_damaged', to='vehicles.sparepart')),
                ('spare_parts_in_stock', models.ManyToManyField(blank=True, related_name='service_shop_spare_parts_in_stock', to='vehicles.sparepart')),
                ('spare_parts_missing', models.ManyToManyField(blank=True, related_name='service_shop_spare_parts_missing', to='vehicles.sparepart')),
                ('vehicles_damaged', models.ManyToManyField(blank=True, related_name='service_shop_vehicles_damaged', to='vehicles.vehicle')),
                ('vehicles_in_stock', models.ManyToManyField(blank=True, related_name='service_shop_vehicles_in_stock', to='vehicles.vehicle')),
                ('vehicles_missing', models.ManyToManyField(blank=True, related_name='service_shop_vehicles_missing', to='vehicles.vehicle')),
            ],
            options={
                'ordering': [django.db.models.functions.text.Lower('warehouse__name')],
            },
        ),
    ]
