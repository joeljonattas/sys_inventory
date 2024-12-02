from django.db import models
from collaborators.models import Collaborator
from django.utils import timezone
from auditlog.registry import auditlog
from categories.models import Category

class LicenseType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

# Create your models here.
class License(models.Model):
    SOFTWARE_CHOICES = [
        ('windows', 'Windows'),
        ('office', 'Microsoft Office'),
        ('adobe', 'Adobe Suite'),
        ('autocad', 'AutoCAD'),
        ('antivirus', 'Antivirus'),
        # Adicione mais conforme necessário
    ]

    STATUS_CHOICES = [
        ('active', 'Ativo'),
        ('in_stock', 'Estoque'),
        ('inactive', 'Inativo'),
    ]

    name = models.CharField(max_length=200, blank=True)
    software = models.CharField(max_length=50, choices=SOFTWARE_CHOICES)
    license_key = models.CharField(max_length=200, unique=True)
    license_type = models.ForeignKey(LicenseType, on_delete=models.PROTECT, related_name='license_type')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='license_category', default='5')
    purchase_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_stock')
    inventory_number = models.CharField(max_length=20, blank=True, unique=True)
    assigned_to = models.ForeignKey(Collaborator, on_delete=models.PROTECT, null=True, blank=True, related_name='collaborator_assigned')
    value = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['status']

    def __str__(self):
        return f'{self.software}'
    
    def is_expired(self):
        if self.expiration_date:
            return self.expiration_date < timezone.now().date()
        
    def save(self, *args, **kwargs):
        if not self.inventory_number:
            next_id = License.objects.count() + 1
            self.inventory_number = f"{next_id:05d}"

        if not self.name:
            self.name = f'LIC-{self.inventory_number}'

        super().save(*args, **kwargs)
        
class LicensesInventory(models.Model):
    licenses_count = models.IntegerField()
    licenses_value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.licenses_count} - {self.licenses_value}'

auditlog.register(License, exclude_fields=['purchase_date', 'expiration_date', 'inventory_number', 'description', 'updated_at', 'created_at'])