# Generated by Django 5.1.2 on 2024-10-31 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printers', '0006_printer_inventory_number_printer_qr_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='printer',
            name='inventory_number',
            field=models.CharField(blank=True, max_length=20, unique=True),
        ),
    ]
