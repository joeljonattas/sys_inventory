# Generated by Django 5.1.2 on 2024-10-16 00:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('computers', '0001_initial'),
        ('phones', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Collaborator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('description', models.TextField(blank=True, max_length=300, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('computer', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='collaborator_computer', to='computers.computer')),
                ('phone', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='collaborator_phone', to='phones.phone')),
                ('phone_number', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='collaborator_number', to='phones.phonenumber')),
                ('sector', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='collaborator_sector', to='collaborators.sector')),
            ],
        ),
    ]
