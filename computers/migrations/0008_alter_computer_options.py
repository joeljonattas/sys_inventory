# Generated by Django 5.1.2 on 2024-11-15 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('computers', '0007_remove_computer_state'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='computer',
            options={'ordering': ['status']},
        ),
    ]
