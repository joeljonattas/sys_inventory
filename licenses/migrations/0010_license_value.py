# Generated by Django 5.1.2 on 2024-10-26 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licenses', '0009_licensesinventory'),
    ]

    operations = [
        migrations.AddField(
            model_name='license',
            name='value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
