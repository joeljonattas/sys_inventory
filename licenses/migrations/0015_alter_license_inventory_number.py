# Generated by Django 5.1.2 on 2024-10-31 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licenses', '0014_alter_license_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='license',
            name='inventory_number',
            field=models.CharField(blank=True, max_length=20, unique=True),
        ),
    ]
