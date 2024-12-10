from django.db import models
from brands.models import Brand
from categories.models import Category
from phonenumber_field.modelfields import PhoneNumberField
from auditlog.registry import auditlog
import qrcode
from io import BytesIO
from django.core.files import File
from django.db.models import Max

class PhoneOperator(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True, max_length=300)

    def __str__(self):
        return self.name

class PhoneNumber(models.Model):
    STATUS_CHOICES = [
        ('active', 'Ativo'),
        ('in_stock', 'Estoque'),
        ('inactive', 'Inativo'),
    ]

    name = models.CharField(max_length=50, blank=True)
    number = PhoneNumberField(region='BR')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_stock')
    operator = models.ForeignKey(PhoneOperator, on_delete=models.PROTECT, related_name='phone_operator')
    value = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    inventory_number = models.CharField(max_length=20, blank=True, unique=True)
    description = models.TextField(blank=True, null=True, max_length=300)

    def __str__(self):
        return str(self.number.as_national)
    
    def save(self, *args, **kwargs):
        if not self.inventory_number:
            last_inventory = PhoneNumber.objects.aggregate(Max('inventory_number'))['inventory_number__max']
            if last_inventory:
                self.inventory_number = f"{int(last_inventory) + 1:05d}"
            else:
                self.inventory_number = "00001"

        if not self.name:
            self.name = f'LT-{self.inventory_number}'

        super().save(*args, **kwargs)
    
class Phone(models.Model):
    STATUS_CHOICES = [
        ('active', 'Ativo'),
        ('in_stock', 'Estoque'),
        ('inactive', 'Inativo'),
    ]

    name = models.CharField(max_length=50, blank=True)
    model = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='phone_brand')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_stock')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='phones_category', default='2')
    number = models.OneToOneField(PhoneNumber, on_delete=models.PROTECT, related_name='phone_number', blank=True, null=True)
    serie_number = models.CharField(max_length=50, blank=True, null=True, unique=True)
    inventory_number = models.CharField(max_length=20, blank=True, unique=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    description = models.TextField(blank=True, null=True, max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['status']

    def __str__(self):
        return f'{self.name}'
    
    def generate_qr_code(self):
        data = (
            f"Propriedade da empresa Sys_Inventory\n\n"
            f"Nome: {self.name}\n"
            f"Serial: {self.serie_number}\n"
            f"Número de Inventário: {self.inventory_number}\n"
            f"CPU: {self.number}\n"
        )

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')

        buffer = BytesIO()
        img.save(buffer, format='PNG')
        file_name = f'qrcode_{self.name}_{self.serie_number}.png'
        self.qr_code.save(file_name, File(buffer), save=False)

    def save(self, *args, **kwargs):
        if not self.inventory_number:
            last_inventory = Phone.objects.aggregate(Max('inventory_number'))['inventory_number__max']
            if last_inventory:
                self.inventory_number = f"{int(last_inventory) + 1:05d}"
            else:
                self.inventory_number = "00001"

        if not self.name:
            self.name = f'TF-{self.inventory_number}'

        super().save(*args, **kwargs)
        if not self.qr_code:
            self.generate_qr_code()
        super().save(*args, **kwargs)
    
class PhonesInventory(models.Model):
    phones_count = models.IntegerField(default=0)
    phones_value = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.phones_count} - {self.phones_value}'
    
class PhonesNumberInventory(models.Model):
    phones_line_count = models.IntegerField(default=0)
    phones_line_value = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.phones_line_count} - {self.phones_line_value}'

auditlog.register(Phone, exclude_fields=['qr_code', 'inventory_number', 'description', 'created_at', 'updated_at'])
auditlog.register(PhoneNumber, exclude_fields=['inventory_number', 'description'])