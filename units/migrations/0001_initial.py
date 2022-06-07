# Generated by Django 4.0.4 on 2022-05-30 17:31

from django.db import migrations, models
import django.db.models.functions.text
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vehicles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('slug', models.SlugField(blank=True)),
                ('name', models.CharField(max_length=60, unique=True)),
                ('location', models.CharField(max_length=60)),
                ('phone_number', models.CharField(blank=True, max_length=13)),
                ('spare_parts_damaged', models.ManyToManyField(blank=True, related_name='warehouse_spare_parts_damaged', to='vehicles.sparepart')),
                ('spare_parts_in_stock', models.ManyToManyField(blank=True, related_name='warehouse_spare_parts_in_stock', to='vehicles.sparepart')),
                ('spare_parts_missing', models.ManyToManyField(blank=True, related_name='warehouse_spare_parts_missing', to='vehicles.sparepart')),
                ('vehicles_damaged', models.ManyToManyField(blank=True, related_name='warehouse_vehicles_damaged', to='vehicles.vehicle')),
                ('vehicles_in_stock', models.ManyToManyField(blank=True, related_name='warehouse_vehicles_in_stock', to='vehicles.vehicle')),
                ('vehicles_missing', models.ManyToManyField(blank=True, related_name='warehouse_vehicles_missing', to='vehicles.vehicle')),
            ],
            options={
                'ordering': [django.db.models.functions.text.Lower('name')],
            },
        ),
        migrations.CreateModel(
            name='ServiceShop',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('slug', models.SlugField(blank=True)),
                ('name', models.CharField(max_length=60, unique=True)),
                ('location', models.CharField(max_length=60)),
                ('phone_number', models.CharField(blank=True, max_length=13)),
                ('spare_parts_damaged', models.ManyToManyField(blank=True, related_name='service_shop_spare_parts_damaged', to='vehicles.sparepart')),
                ('spare_parts_in_stock', models.ManyToManyField(blank=True, related_name='service_shop_spare_parts_in_stock', to='vehicles.sparepart')),
                ('spare_parts_missing', models.ManyToManyField(blank=True, related_name='service_shop_spare_parts_missing', to='vehicles.sparepart')),
                ('vehicles_damaged', models.ManyToManyField(blank=True, related_name='service_shop_vehicles_damaged', to='vehicles.vehicle')),
                ('vehicles_in_stock', models.ManyToManyField(blank=True, related_name='service_shop_vehicles_in_stock', to='vehicles.vehicle')),
                ('vehicles_missing', models.ManyToManyField(blank=True, related_name='service_shop_vehicles_missing', to='vehicles.vehicle')),
            ],
            options={
                'ordering': [django.db.models.functions.text.Lower('name')],
            },
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('slug', models.SlugField(blank=True)),
                ('name', models.CharField(max_length=60, unique=True)),
                ('location', models.CharField(max_length=60)),
                ('phone_number', models.CharField(blank=True, max_length=13)),
                ('spare_parts_damaged', models.ManyToManyField(blank=True, related_name='branch_spare_parts_damaged', to='vehicles.sparepart')),
                ('spare_parts_in_stock', models.ManyToManyField(blank=True, related_name='branch_spare_parts_in_stock', to='vehicles.sparepart')),
                ('spare_parts_missing', models.ManyToManyField(blank=True, related_name='branch_spare_parts_missing', to='vehicles.sparepart')),
                ('vehicles_damaged', models.ManyToManyField(blank=True, related_name='branch_vehicles_damaged', to='vehicles.vehicle')),
                ('vehicles_in_stock', models.ManyToManyField(blank=True, related_name='branch_vehicles_in_stock', to='vehicles.vehicle')),
                ('vehicles_missing', models.ManyToManyField(blank=True, related_name='branch_vehicles_missing', to='vehicles.vehicle')),
            ],
            options={
                'ordering': [django.db.models.functions.text.Lower('name')],
            },
        ),
    ]
