from computers.models import ComputersInventory, Computer
from phones.models import PhonesInventory, PhonesNumberInventory, Phone, PhoneNumber
from printers.models import Printer, PrintersInventory
from licenses.models import License, LicensesInventory
from categories.models import Category
from brands.models import Brand
from collaborators.models import Sector
from django.utils.formats import number_format
from django.utils import timezone
from django.db.models import Count, Q
import json

def get_inventory_metrics():
    latest_computers = ComputersInventory.objects.latest('created_at')
    latest_phones = PhonesInventory.objects.latest('created_at')
    latest_lines = PhonesNumberInventory.objects.latest('created_at')
    latest_printers = PrintersInventory.objects.latest('created_at')
    latest_licenses = LicensesInventory.objects.latest('created_at')

    data = {
        'computers_quantity': latest_computers.computers_count,
        'computers_value': number_format(latest_computers.computers_value, decimal_pos=2, force_grouping=True),

        'phones_quantity': latest_phones.phones_count,
        'phones_value': number_format(latest_phones.phones_value, decimal_pos=2, force_grouping=True),

        'phones_lines_quantity': latest_lines.phones_line_count,
        'phones_lines_value': number_format(latest_lines.phones_line_value, decimal_pos=2, force_grouping=True),

        'printers_quantity': latest_printers.printers_count,
        'printers_value': number_format(latest_printers.printers_value, decimal_pos=2, force_grouping=True),

        'licenses_quantity': latest_licenses.licenses_count,
        'licenses_value': number_format(latest_licenses.licenses_value, decimal_pos=2, force_grouping=True),

        'inventory_value': number_format(
            latest_computers.computers_value +
            latest_phones.phones_value +
            latest_lines.phones_line_value,
            decimal_pos=2,
            force_grouping=True
        ),
    }

    return data

def get_brand_equipaments():
    brands = Brand.objects.all()
    brand_names = [brand.name for brand in brands]
    brand_count_equipaments = [brand.equipament_count for brand in brands]

    data = {
        'brand_names': json.dumps(brand_names),
        'brand_count_equipaments': json.dumps(brand_count_equipaments),
    }

    return data


def get_status_equipaments():
    equipaments = [Computer, Phone, Printer, License, PhoneNumber]

    STATUS_CHOICES = [
        ('active', 'Ativo'),
        ('in_stock', 'Estoque'),
        ('inactive', 'Inativo'),
    ]

    status_count = {status[0]: 0 for status in STATUS_CHOICES}
    
    for model in equipaments:
        status_counts = model.objects.values('status').annotate(count=Count('status'))
        for item in status_counts:
            status_count[item['status']] += item['count']

    status_names = [dict(STATUS_CHOICES)[key] for key in status_count.keys()]
    status_count_equipments = list(status_count.values())

    print(status_names)
    print(status_count_equipments)
    
    data = {
        'status_names': json.dumps(status_names),
        'status_count_equipaments': json.dumps(status_count_equipments),
    }

    return data

def get_sectors_equipaments():
    sectors = Sector.objects.all()

    # Calcula a contagem de cada tipo de equipamento por setor
    sectors_data = list(sectors.annotate(
        computers=Count('collaborator_sector__computer', filter=Q(collaborator_sector__computer__isnull=False)),
        phones=Count('collaborator_sector__phone', filter=Q(collaborator_sector__phone__isnull=False)),
        phone_numbers=Count('collaborator_sector__phone_number', filter=Q(collaborator_sector__phone_number__isnull=False))
    ).values('name', 'computers', 'phones', 'phone_numbers'))

    # Dados para enviar ao frontend
    data = {
        'sectors_data': json.dumps(sectors_data)  # Cada setor com seus respectivos totais de equipamento
    }

    return data

def get_daily_register():
    today = timezone.localtime().date()
    dates = [str(today - timezone.timedelta(days=i)) for i in range(6, -1, -1)]
    models = ['Computadores', 'Telefones', 'Linhas Telefonicas', 'Impressoras', 'Licencas']
    data = {
        'dates': json.dumps(dates),
        'models': json.dumps(models),
    }

    computer_values = []
    phone_values = []
    printers_values = []
    licenses_values = []

    for date in dates:
        computer_values.append(Computer.objects.filter(created_at__date=date).count())
        phone_values.append(Phone.objects.filter(created_at__date=date).count())
        printers_values.append(Printer.objects.filter(created_at__date=date).count())
        licenses_values.append(License.objects.filter(created_at__date=date).count())


    data['computer_values'] = json.dumps(computer_values)
    data['phone_values'] = json.dumps(phone_values)
    data['printers_values'] = json.dumps(printers_values)
    data['licenses_values'] = json.dumps(licenses_values)

    return data