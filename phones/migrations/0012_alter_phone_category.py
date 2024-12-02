# Generated by Django 5.1.2 on 2024-11-23 12:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0003_alter_category_equipament_count'),
        ('phones', '0011_alter_phone_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phone',
            name='category',
            field=models.ForeignKey(default='2', on_delete=django.db.models.deletion.PROTECT, related_name='phones_category', to='categories.category'),
        ),
    ]