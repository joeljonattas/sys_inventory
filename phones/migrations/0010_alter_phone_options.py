# Generated by Django 5.1.2 on 2024-11-15 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phones', '0009_phonenumber_inventory_number_phonenumber_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='phone',
            options={'ordering': ['status']},
        ),
    ]
