# Generated by Django 4.0.4 on 2022-06-17 19:31

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.functions.text
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=150)),
                ('address', models.CharField(max_length=150)),
                ('location', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=15)),
                ('email', models.CharField(blank=True, max_length=200)),
                ('consumption_type', models.CharField(blank=True, choices=[('finance sale', 'Finance Sale'), ('corporate sale', 'Corporate Sale')], default=None, max_length=50, null=True)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': [django.db.models.functions.text.Lower('name')],
            },
        ),
        migrations.RenameField(
            model_name='financeandcorporatesale',
            old_name='customer_type',
            new_name='sale_type',
        ),
        migrations.RemoveField(
            model_name='financeandcorporatesale',
            name='customer',
        ),
        migrations.AlterField(
            model_name='customer',
            name='customer_type',
            field=models.CharField(blank=True, choices=[('retail', 'Retail'), ('wholesale', 'Wholesale')], default=None, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='financeandcorporatesale',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.organization'),
        ),
    ]
