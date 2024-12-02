# Generated by Django 5.1.2 on 2024-10-16 23:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('collaborators', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LicenseType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('software', models.CharField(choices=[('windows', 'Windows'), ('office', 'Microsoft Office'), ('adobe', 'Adobe Suite'), ('autocad', 'AutoCAD'), ('antivirus', 'Antivirus')], max_length=50)),
                ('license_key', models.CharField(max_length=200, unique=True)),
                ('purchase_date', models.DateField(blank=True, null=True)),
                ('expiration_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('active', 'Ativo'), ('in_stock', 'Estoque'), ('inactive', 'Inativo')], max_length=20)),
                ('description', models.TextField(blank=True, null=True)),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='collaborator_assigned', to='collaborators.collaborator')),
                ('license_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='license_type', to='licenses.licensetype')),
            ],
        ),
    ]