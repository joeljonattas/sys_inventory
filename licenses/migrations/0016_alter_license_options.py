# Generated by Django 5.1.2 on 2024-11-15 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('licenses', '0015_alter_license_inventory_number'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='license',
            options={'ordering': ['status']},
        ),
    ]
