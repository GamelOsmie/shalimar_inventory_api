# Generated by Django 4.0.4 on 2022-05-17 17:36

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.functions.text
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('slug', models.SlugField(blank=True)),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'ordering': [django.db.models.functions.text.Lower('name')],
            },
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('slug', models.SlugField(blank=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('purchase_price', models.IntegerField(blank=True, default=0)),
                ('retail_price', models.IntegerField(blank=True, default=0)),
                ('wholesale_price', models.IntegerField(blank=True, default=0)),
                ('finance_sale_price', models.IntegerField(blank=True, default=0)),
                ('corporate_sale_price', models.IntegerField(blank=True, default=0)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='brands', to='vehicles.brand')),
            ],
            options={
                'ordering': [django.db.models.functions.text.Lower('brand__name')],
            },
        ),
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.CharField(default=0, max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('slug', models.SlugField(blank=True)),
                ('chassis_number', models.CharField(max_length=50, unique=True)),
                ('engine_number', models.CharField(max_length=30, unique=True)),
                ('color', models.CharField(blank=True, max_length=30)),
                ('current_location', models.CharField(choices=[('at sea', 'At Sea'), ('warehouse', 'Warehouse'), ('branch', 'Branch'), ('service station', 'Service Station'), ('finance sale', 'Finance Sale'), ('corporate sale', 'Corporate Sale'), ('wholesale', 'Wholesale'), ('retail', 'Retail'), ('missing', 'Missing')], default='at sea', max_length=20)),
                ('custodian', models.CharField(blank=True, max_length=100)),
                ('last_moved', models.DateTimeField(auto_now=True)),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='models', to='vehicles.model')),
            ],
            options={
                'ordering': [django.db.models.functions.text.Lower('model__brand')],
            },
        ),
        migrations.CreateModel(
            name='SparePartType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('slug', models.SlugField(blank=True)),
                ('part', models.CharField(max_length=100)),
                ('purchase_price', models.IntegerField(blank=True, default=0)),
                ('retail_price', models.IntegerField(blank=True, default=0)),
                ('wholesale_price', models.IntegerField(blank=True, default=0)),
                ('finance_sale_price', models.IntegerField(blank=True, default=0)),
                ('corporate_sale_price', models.IntegerField(blank=True, default=0)),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sparepart_models', to='vehicles.model')),
                ('tax', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='vehicles.tax')),
            ],
            options={
                'ordering': [django.db.models.functions.text.Lower('model__brand')],
            },
        ),
        migrations.CreateModel(
            name='SparePart',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('slug', models.SlugField(blank=True)),
                ('part_number', models.CharField(max_length=30, unique=True)),
                ('current_location', models.CharField(choices=[('at sea', 'At Sea'), ('warehouse', 'Warehouse'), ('branch', 'Branch'), ('finance sale', 'Finance Sale'), ('corporate sale', 'Corporate Sale'), ('wholesale', 'Wholesale'), ('retail', 'Retail')], default=None, max_length=20)),
                ('custodian', models.CharField(blank=True, max_length=100, null=True)),
                ('last_moved', models.DateTimeField(auto_now=True)),
                ('part_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sparepart_type', to='vehicles.spareparttype')),
            ],
            options={
                'ordering': [django.db.models.functions.text.Lower('part_number')],
            },
        ),
        migrations.AddField(
            model_name='model',
            name='tax',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='vehicles.tax'),
        ),
    ]
