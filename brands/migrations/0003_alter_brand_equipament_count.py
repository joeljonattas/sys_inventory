# Generated by Django 5.1.2 on 2024-10-28 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brands', '0002_brand_equipament_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='equipament_count',
            field=models.IntegerField(),
        ),
    ]