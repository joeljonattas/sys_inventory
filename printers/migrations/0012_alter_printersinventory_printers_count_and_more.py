# Generated by Django 5.1.2 on 2024-12-02 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printers', '0011_alter_printer_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='printersinventory',
            name='printers_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='printersinventory',
            name='printers_value',
            field=models.FloatField(default=0),
        ),
    ]
