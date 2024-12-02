# Generated by Django 5.1.2 on 2024-10-31 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phones', '0008_alter_phone_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='phonenumber',
            name='inventory_number',
            field=models.CharField(blank=True, max_length=20, unique=True),
        ),
        migrations.AddField(
            model_name='phonenumber',
            name='name',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
