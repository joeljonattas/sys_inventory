# Generated by Django 5.1.2 on 2024-10-20 17:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('printers', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='printer',
            old_name='serial_number',
            new_name='serie_number',
        ),
    ]