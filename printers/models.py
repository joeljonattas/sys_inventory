from django.db import models
from brands.models import Brand
from categories.models import Category
from collaborators.models import Sector
from auditlog.registry import auditlog
import qrcode
from io import BytesIO
from django.core.files import File
from django.db.models import Max

# Create your models here.
class Printer(models.Model):
    STATUS_CHOICES = [
        ('active', 'Ativo'),
        ('in_stock', 'Estoque'),
        ('inactive', 'Inativo'),
    ]

    name = models.CharField(max_length=50, blank=True)
    model = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='printers_brand')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='printers_category', default='3')
    serie_number = models.CharField(max_length=50, blank=True, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_stock')
    inventory_number = models.CharField(max_length=20, blank=True, unique=True)
    location = models.ForeignKey(Sector, on_delete=models.PROTECT, related_name='printers_location')
    address = models.GenericIPAddressField(blank=True, null=True, unique=True)
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
            f"Localização: {self.location}\n"
            f"Endereço IP: {self.address}\n"
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
            last_inventory = Printer.objects.aggregate(Max('inventory_number'))['inventory_number__max']
            if last_inventory:
                self.inventory_number = f"{int(last_inventory) + 1:05d}"
            else:
                self.inventory_number = "00001"

        if not self.name:
            self.name = f'IMP-{self.inventory_number}'

        super().save(*args, **kwargs)
        if not self.qr_code:
            self.generate_qr_code()
        super().save(*args, **kwargs)
    
    
class PrintersInventory(models.Model):
    printers_count = models.IntegerField()
    printers_value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.printers_count} - {self.printers_value}'

auditlog.register(Printer, exclude_fields=['qr_code', 'inventory_number', 'description', 'updated_at', 'created_at'])