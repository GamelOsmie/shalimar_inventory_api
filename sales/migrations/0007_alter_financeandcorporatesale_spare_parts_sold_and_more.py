# Generated by Django 4.0.4 on 2022-07-07 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0003_alter_sparepart_current_location_and_more'),
        ('sales', '0006_alter_financeandcorporatesale_organization_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='financeandcorporatesale',
            name='spare_parts_sold',
            field=models.ManyToManyField(blank=True, related_name='finance_and_corporate_spare_part_sales', to='vehicles.sparepart'),
        ),
        migrations.AlterField(
            model_name='wholesale',
            name='spare_parts_sold',
            field=models.ManyToManyField(blank=True, related_name='wholesale_spare_part_sales', to='vehicles.sparepart'),
        ),
    ]