# Generated by Django 5.1.2 on 2024-11-15 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printers', '0009_alter_printer_options_alter_printer_serie_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='printer',
            name='serie_number',
            field=models.CharField(blank=True, max_length=50, unique=True),
        ),
    ]