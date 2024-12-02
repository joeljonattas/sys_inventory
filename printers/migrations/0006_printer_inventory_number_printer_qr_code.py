# Generated by Django 5.1.2 on 2024-10-31 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printers', '0005_remove_printer_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='printer',
            name='inventory_number',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='printer',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to='qrcodes/'),
        ),
    ]
