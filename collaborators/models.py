from django.db import models
from computers.models import Computer
from phones.models import Phone
from phones.models import PhoneNumber
from auditlog.registry import auditlog

# Create your models here.
class Sector(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True, max_length=300)

    def __str__(self):
        return self.name
    

class Collaborator(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, blank=False, null=False, unique=True)
    sector = models.ForeignKey(Sector, on_delete=models.PROTECT, related_name='collaborator_sector')
    computer = models.OneToOneField(Computer, on_delete=models.PROTECT, related_name='collaborator_computer', blank=True, null=True)
    phone = models.OneToOneField(Phone, on_delete=models.PROTECT, related_name='collaborator_phone', blank=True, null=True)
    phone_number = models.OneToOneField(PhoneNumber, on_delete=models.PROTECT, related_name='collaborator_number', blank=True, null=True)
    description = models.TextField(blank=True, null=True, max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

auditlog.register(Collaborator)