# Generated by Django 4.0.4 on 2022-07-08 05:33

from django.db import migrations, models
import django.db.models.deletion
import operations.models
import shortuuid.django_fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vehicles', '0001_initial'),
        ('units', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommercialInvoice',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('invoice_number', models.CharField(max_length=30, unique=True)),
                ('invoice_date', models.DateField()),
                ('document', models.FileField(upload_to='invoices/commercial')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-uploaded_at'],
            },
        ),
        migrations.CreateModel(
            name='Container',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('slug', models.SlugField(blank=True)),
                ('container_number', models.CharField(max_length=20, unique=True)),
                ('content_type', models.CharField(blank=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ProformaInvoice',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('invoice_number', models.CharField(max_length=30, unique=True)),
                ('invoice_date', models.DateField()),
                ('document', models.FileField(upload_to='invoices/proforma')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-uploaded_at'],
            },
        ),
        migrations.CreateModel(
            name='WarehouseVehiclesSupply',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('slug', models.SlugField(blank=True)),
                ('supply_code', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', editable=False, length=7, max_length=10, prefix='WVS', unique=True)),
                ('vehicles_supplied_quantity', models.CharField(blank=True, max_length=10)),
                ('vehicles_supplied_received', models.CharField(blank=True, default=0, max_length=10)),
                ('supply_date', models.DateTimeField(auto_now_add=True)),
                ('received_date', models.DateTimeField(blank=True, null=True)),
                ('container', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='container_vehicles', to='operations.container')),
                ('vehicles_supplied', models.ManyToManyField(blank=True, related_name='warehouse_vehicles_supplied', to='vehicles.vehicle')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='vehicle_warehouses', to='units.warehouse')),
            ],
            options={
                'ordering': ['-supply_date'],
            },
        ),
        migrations.CreateModel(
            name='WarehouseSparePartsSupply',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('slug', models.SlugField(blank=True)),
                ('supply_code', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', editable=False, length=7, max_length=10, prefix='WPS', unique=True)),
                ('spare_parts_supplied_quantity', models.CharField(blank=True, max_length=10)),
                ('spare_parts_supplied_received', models.CharField(blank=True, default=0, max_length=10)),
                ('supply_date', models.DateTimeField(auto_now_add=True)),
                ('received_date', models.DateTimeField(blank=True, null=True)),
                ('container', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='container_spare_parts', to='operations.container')),
                ('spare_parts_supplied', models.ManyToManyField(blank=True, related_name='warehouse_spare_parts_supplied', to='vehicles.sparepart')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='spare_part_warehouses', to='units.warehouse')),
            ],
            options={
                'ordering': ['-supply_date'],
            },
        ),
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('slug', models.SlugField(blank=True)),
                ('batch_number', models.CharField(max_length=20)),
                ('eta', models.DateField()),
                ('port_of_origin', models.CharField(max_length=250)),
                ('port_of_destination', models.CharField(max_length=250)),
                ('clearing_agent', models.CharField(max_length=50)),
                ('bill_of_lading_number', models.CharField(max_length=50, unique='true')),
                ('departs_embarkation_port', models.JSONField(default=operations.models.Shipment.default_journey_state)),
                ('container_docks_at_disembarkation_port', models.JSONField(default=operations.models.Shipment.default_journey_state)),
                ('declaration_of_invoice_for_payment', models.JSONField(default=operations.models.Shipment.default_journey_state)),
                ('make_ctn_payment', models.JSONField(default=operations.models.Shipment.default_journey_state)),
                ('intertek_payment', models.JSONField(default=operations.models.Shipment.default_journey_state)),
                ('delivery_order_payment', models.JSONField(default=operations.models.Shipment.default_journey_state)),
                ('port_charges_payment', models.JSONField(default=operations.models.Shipment.default_journey_state)),
                ('container_scan', models.JSONField(default=operations.models.Shipment.default_journey_state)),
                ('asycuda_system_input', models.JSONField(default=operations.models.Shipment.default_journey_state)),
                ('examination_of_goods', models.JSONField(default=operations.models.Shipment.default_journey_state)),
                ('release_order_given_at_the_port', models.JSONField(default=operations.models.Shipment.default_journey_state)),
                ('container_exist_port', models.JSONField(default=operations.models.Shipment.default_journey_state)),
                ('container_arrives_at_warehouse', models.JSONField(default=operations.models.Shipment.default_journey_state)),
                ('container_offloaded', models.JSONField(default=operations.models.Shipment.default_journey_state)),
                ('container_to_shipping', models.JSONField(default=operations.models.Shipment.default_journey_state)),
                ('confirmation_of_vehicle_quantity', models.JSONField(default=operations.models.Shipment.default_journey_state)),
                ('on_the_move', models.BooleanField(default=False)),
                ('departed_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('commercial_invoice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='shipments_commercial_invoices', to='operations.commercialinvoice')),
                ('proforma_invoice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='shipments_proforma_invoices', to='operations.proformainvoice')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='container',
            name='shipment_batch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='contains', to='operations.shipment'),
        ),
        migrations.AddField(
            model_name='container',
            name='spare_parts',
            field=models.ManyToManyField(blank=True, related_name='container_spare_parts', to='vehicles.sparepart'),
        ),
        migrations.AddField(
            model_name='container',
            name='vehicles',
            field=models.ManyToManyField(blank=True, related_name='container_vehicles', to='vehicles.vehicle'),
        ),
        migrations.AddField(
            model_name='commercialinvoice',
            name='linked_proforma_invoice',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='commercial_invoices', to='operations.proformainvoice'),
        ),
        migrations.CreateModel(
            name='BranchVehiclesSupply',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('slug', models.SlugField(blank=True)),
                ('supply_code', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', editable=False, length=7, max_length=10, prefix='BVS', unique=True)),
                ('vehicles_supplied_quantity', models.CharField(blank=True, max_length=10)),
                ('vehicles_supplied_received', models.CharField(blank=True, default=0, max_length=10)),
                ('supply_date', models.DateTimeField(auto_now_add=True)),
                ('received_date', models.DateTimeField(blank=True, null=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='vehicle_branches', to='units.branch')),
                ('vehicles_supplied', models.ManyToManyField(blank=True, related_name='branch_vehicles_supplied', to='vehicles.vehicle')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='warehouse_vehicles_for_supply', to='units.warehouse')),
            ],
            options={
                'ordering': ['-supply_date'],
            },
        ),
        migrations.CreateModel(
            name='BranchSparePartsSupply',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('slug', models.SlugField(blank=True)),
                ('supply_code', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', editable=False, length=7, max_length=10, prefix='BPS', unique=True)),
                ('spare_parts_supplied_quantity', models.CharField(blank=True, max_length=10)),
                ('spare_parts_supplied_received', models.CharField(blank=True, default=0, max_length=10)),
                ('supply_date', models.DateTimeField(auto_now_add=True)),
                ('received_date', models.DateTimeField(blank=True, null=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='spare_part_branches', to='units.branch')),
                ('spare_parts_supplied', models.ManyToManyField(blank=True, related_name='branch_vehicles_supplied', to='vehicles.sparepart')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='warehouse_spare_part_for_supply', to='units.warehouse')),
            ],
            options={
                'ordering': ['-supply_date'],
            },
        ),
    ]
