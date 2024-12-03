from django.db import models
from brands.models import Brand
from categories.models import Category
from auditlog.registry import auditlog
import qrcode
from io import BytesIO
from django.core.files import File
from django.db.models import Max

# Create your models here.
class Computer(models.Model):
    STATUS_CHOICES = [
        ('active', 'Ativo'),
        ('in_stock', 'Estoque'),
        ('inactive', 'Inativo'),
    ]

    RAM_CHOICES = [
        ('2GB', '2GB'),
        ('4GB', '4GB'),
        ('8GB', '8GB'),
        ('12GB', '12GB'),
        ('16GB', '16GB'),
        ('32GB', '32GB'),
        ('64GB', '64GB'),
        ('128GB', '128GB'),
        ('256GB', '256GB'),
    ]

    STORAGE_CHOICES = [
        ('128GB SSD', '128GB SSD'),
        ('256GB SSD', '256GB SSD'),
        ('480GB SSD', '480GB SSD'),
        ('512GB SSD', '512GB SSD'),
        ('1TB SSD', '1TB SSD'),
        ('128GB HD', '128GB HD'),
        ('256GB HD', '256GB HD'),
        ('480GB HD', '480GB HD'),
        ('512GB HD', '512GB HD'),
        ('1TB HDD', '1TB HDD'),
    ]

    name = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=100, blank=False, null=False)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='computer_brand')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='computer_category')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_stock')
    serie_number = models.CharField(max_length=50, blank=True, null=True, unique=True)
    inventory_number = models.CharField(max_length=20, blank=True, unique=True)
    cpu = models.CharField(max_length=100, blank=True, null=True)
    memory_ram = models.CharField(max_length=10, choices=RAM_CHOICES, blank=True, null=True)
    storage = models.CharField(max_length=10, choices=STORAGE_CHOICES, blank=True, null=True)
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
            f"CPU: {self.cpu}\n"
            f"Memória RAM: {self.memory_ram}\n"
            f"Armazenamento: {self.storage}"
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
            last_inventory = Computer.objects.aggregate(Max('inventory_number'))['inventory_number__max']
            if last_inventory:
                self.inventory_number = f"{int(last_inventory) + 1:05d}"
            else:
                self.inventory_number = "00001"

        if not self.name:
            self.name = f'PC-{self.inventory_number}'

        super().save(*args, **kwargs)
        if not self.qr_code:
            self.generate_qr_code()
        super().save(*args, **kwargs)
    
class ComputersInventory(models.Model):
    computers_count = models.IntegerField(default=0)
    computers_value = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.computers_count} - {self.computers_value}'


auditlog.register(Computer, exclude_fields=['qr_code', 'inventory_number'])