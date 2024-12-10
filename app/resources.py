from collaborators.models import Collaborator, Sector
from computers.models import Computer
from phones.models import Phone, PhoneNumber, PhoneOperator
from import_export import resources, fields, widgets
from import_export.widgets import ForeignKeyWidget
from categories.models import Category
from brands.models import Brand
from licenses.models import License, LicenseType
from printers.models import Printer
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta

class CollaboratorResource(resources.ModelResource):
    sector = fields.Field(
        column_name='Setor',
        attribute='sector',
        widget=ForeignKeyWidget(Sector, field='name')
    )

    computer = fields.Field(
        column_name='Computador',
        attribute='computer',
        widget=ForeignKeyWidget(Computer, field='model')
    )

    phone = fields.Field(
        column_name='Telefone',
        attribute='phone',
        widget=ForeignKeyWidget(Phone, field='model')
    )

    phone_number = fields.Field(
        column_name='Linha Telefônica',
        attribute='phone_number',
        widget=ForeignKeyWidget(PhoneNumber, field='number')
    )

    name = fields.Field(
        column_name='Nome',
        attribute='name'
    )

    email = fields.Field(
        column_name='E-mail',
        attribute='email'
    )

    description = fields.Field(
        column_name='Descrição',
        attribute='description'
    )

    class Meta:
        model = Collaborator
        fields = (
            'name',
            'email',
            'sector',
            'computer',
            'phone',
            'phone_number',
            'description',
        )

class CollaboratorImportResource(resources.ModelResource):

    name = fields.Field(
        column_name='nome',
        attribute='name'
    )

    description = fields.Field(
        column_name='descricao',
        attribute='description'
    )

    sector = fields.Field(
        column_name='setor',
        attribute='sector',
        widget=ForeignKeyWidget(Sector, field='name')
    )


    class Meta:
        model = Collaborator
        fields = ('name', 'email', 'sector', 'description')
        import_id_fields = ('email',)

    def before_import_row(self, row, **kwargs):
        email = row.get('email')
        if email and Collaborator.objects.filter(email=email).exists():
            raise ValidationError(f"O E-mail '{email}' já está cadastrado.")

class ComputerResource(resources.ModelResource):

    brand = fields.Field(
        column_name='Fabricante',
        attribute='brand',
        widget=ForeignKeyWidget(Brand, field='name')
    )

    category = fields.Field(
        column_name='Categoria',
        attribute='category',
        widget=ForeignKeyWidget(Category, field='name')
    )

    status = fields.Field(
        column_name='Status',
        attribute='status',
        widget=widgets.CharWidget()
    )

    name = fields.Field(
        column_name='Nome',
        attribute='name',
    )

    model = fields.Field(
        column_name='Modelo',
        attribute='model'
    )

    inventory_number = fields.Field(
        column_name='Nº de Inventário',
        attribute='inventory_number'
    )

    serie_number = fields.Field(
        column_name='Nº de Série',
        attribute='serie_number'
    )

    value = fields.Field(
        column_name='Valor',
        attribute='value'
    )

    description = fields.Field(
        column_name='Descrição',
        attribute='descripition'
    )

    cpu = fields.Field(
        column_name='Processador',
        attribute='cpu'
    )

    memory_ram = fields.Field(
        column_name='Memória RAM',
        attribute='memory_ram'
    )

    storage = fields.Field(
        column_name='Armazenamento',
        attribute='storage'
    )

    class Meta:
        model = Computer
        fields = ('name', 'model', 'inventory_number', 'brand', 'category', 'serie_number', 'status', 'cpu', 'memory_ram', 'storage', 'value', 'description')
        import_id_fields = ('serie_number',)

    def dehydrate_status(self, computer):
        return computer.get_status_display()

    def before_import_row(self, row, **kwargs):
        status_map = {v: k for k, v in Computer.STATUS_CHOICES}
        if 'status' in row and row['status'] in status_map:
            row['status'] = status_map[row['status']]

class ComputerImportResource(resources.ModelResource):

    brand = fields.Field(
        column_name='fabricante',
        attribute='brand',
        widget=ForeignKeyWidget(Brand, field='name')
    )

    category = fields.Field(
        column_name='categoria',
        attribute='category',
        widget=ForeignKeyWidget(Category, field='name')
    )

    serie_number = fields.Field(
        column_name='numero_serie',
        attribute='serie_number'
    )

    status = fields.Field(
        column_name='status',
        attribute='status',
        widget=widgets.CharWidget()
    )

    model = fields.Field(
        column_name='modelo',
        attribute='model'
    )

    value = fields.Field(
        column_name='valor',
        attribute='value'
    )

    description = fields.Field(
        column_name='descricao',
        attribute='descripition'
    )

    cpu = fields.Field(
        column_name='processador',
        attribute='cpu'
    )

    memory_ram = fields.Field(
        column_name='memoria_ram',
        attribute='memory_ram',
        widget=widgets.CharWidget()
    )

    storage = fields.Field(
        column_name='armazenamento',
        attribute='storage',
        widget=widgets.CharWidget()
    )

    class Meta:
        model = Computer
        fields = ('model', 'brand', 'category', 'serie_number', 'status', 'cpu', 'memory_ram', 'storage', 'value', 'description')
        import_id_fields = ('serie_number',)

    def dehydrate_status(self, computer):
        return computer.get_status_display()

    def before_import_row(self, row, **kwargs):
        status_map = {v: k for k, v in Computer.STATUS_CHOICES}
        if 'status' in row and row['status'] in status_map:
            row['status'] = status_map[row['status']]

        serie_number = row.get('numero_serie')
        if serie_number and Computer.objects.filter(serie_number=serie_number).exists():
            raise ValidationError(f"O número de série '{serie_number}' já está cadastrado.")

class PhoneResource(resources.ModelResource):

    brand = fields.Field(
        column_name='Fabricante',
        attribute='brand',
        widget=ForeignKeyWidget(Brand, field='name')
    )

    category = fields.Field(
        column_name='Categoria',
        attribute='category',
        widget=ForeignKeyWidget(Category, field='name')
    )

    status = fields.Field(
        column_name='Status',
        attribute='status',
        widget=widgets.CharWidget()
    )

    name = fields.Field(
        column_name='Nome',
        attribute='name',
    )

    model = fields.Field(
        column_name='Modelo',
        attribute='model'
    )

    inventory_number = fields.Field(
        column_name='Nº de Inventário',
        attribute='inventory_number'
    )

    serie_number = fields.Field(
        column_name='Nº de Série',
        attribute='serie_number'
    )

    value = fields.Field(
        column_name='Valor',
        attribute='value'
    )

    description = fields.Field(
        column_name='Descrição',
        attribute='descripition'
    )

    number = fields.Field(
        column_name='Nº de Telefone',
        attribute='number',
        widget=ForeignKeyWidget(PhoneNumber, field='number')
    )
    class Meta:
        model = Phone
        fields = ('name', 'model', 'inventory_number', 'brand', 'category', 'serie_number', 'number', 'status', 'value', 'description')
        import_id_fields = ('serie_number',)

    def dehydrate_status(self, phone):
        return phone.get_status_display()

    def before_import_row(self, row, **kwargs):
        status_map = {v: k for k, v in Phone.STATUS_CHOICES}
        if 'status' in row and row['status'] in status_map:
            row['status'] = status_map[row['status']]

class PhoneImportResource(resources.ModelResource):

    brand = fields.Field(
        column_name='fabricante',
        attribute='brand',
        widget=ForeignKeyWidget(Brand, field='name')
    )

    category = fields.Field(
        column_name='categoria',
        attribute='category',
        widget=ForeignKeyWidget(Category, field='name')
    )

    serie_number = fields.Field(
        column_name='numero_serie',
        attribute='serie_number'
    )

    status = fields.Field(
        column_name='status',
        attribute='status',
        widget=widgets.CharWidget()
    )

    model = fields.Field(
        column_name='modelo',
        attribute='model'
    )

    value = fields.Field(
        column_name='valor',
        attribute='value'
    )

    description = fields.Field(
        column_name='descricao',
        attribute='descripition'
    )

    class Meta:
        model = Phone
        fields = ('model', 'brand', 'category', 'serie_number', 'status', 'value', 'description')
        import_id_fields = ('serie_number',)

    def dehydrate_status(self, phone):
        return phone.get_status_display()

    def before_import_row(self, row, **kwargs):
        status_map = {v: k for k, v in Phone.STATUS_CHOICES}
        if 'status' in row and row['status'] in status_map:
            row['status'] = status_map[row['status']]

        serie_number = row.get('numero_serie')
        if serie_number and Computer.objects.filter(serie_number=serie_number).exists():
            raise ValidationError(f"O número de série '{serie_number}' já está cadastrado.")

class PhoneNumberResource(resources.ModelResource):

    status = fields.Field(
        column_name='Status',
        attribute='status',
        widget=widgets.CharWidget()
    )

    operator = fields.Field(
        column_name='Operadora',
        attribute='operator',
        widget=ForeignKeyWidget(PhoneOperator, field='name')
    )

    value = fields.Field(
        column_name='Valor',
        attribute='value'
    )

    description = fields.Field(
        column_name='Descrição',
        attribute='descripition'
    )

    number = fields.Field(
        column_name='Nº de Telefone',
        attribute='number',
    )

    name = fields.Field(
        column_name='Nome',
        attribute='name',
    )

    inventory_number = fields.Field(
        column_name='Nº de Inventário',
        attribute='inventory_number'
    )

    class Meta:
        model = PhoneNumber
        fields = ('name', 'number', 'status', 'inventory_number', 'operator', 'value', 'description')
        import_id_fields = ('number',)

    def dehydrate_status(self, phone_number):
        return phone_number.get_status_display()

    def before_import_row(self, row, **kwargs):
        status_map = {v: k for k, v in PhoneNumber.STATUS_CHOICES}
        if 'status' in row and row['status'] in status_map:
            row['status'] = status_map[row['status']]

class PhoneNumberImportResource(resources.ModelResource):

    status = fields.Field(
        column_name='status',
        attribute='status',
        widget=widgets.CharWidget()
    )

    operator = fields.Field(
        column_name='operadora',
        attribute='operator',
        widget=ForeignKeyWidget(PhoneOperator, field='name')
    )

    value = fields.Field(
        column_name='valor',
        attribute='value'
    )

    description = fields.Field(
        column_name='descricao',
        attribute='descripition'
    )

    number = fields.Field(
        column_name='numero_telefone',
        attribute='number',
    )

    class Meta:
        model = PhoneNumber
        fields = ('number', 'status', 'operator', 'value', 'description')
        import_id_fields = ('number',)

    def dehydrate_status(self, phone_number):
        return phone_number.get_status_display()

    def before_import_row(self, row, **kwargs):
        status_map = {v: k for k, v in PhoneNumber.STATUS_CHOICES}
        if 'status' in row and row['status'] in status_map:
            row['status'] = status_map[row['status']]

        number = row.get('numero_telefone')
        if number and Printer.objects.filter(number=number).exists():
            raise ValidationError(f"O número de série '{number}' já está cadastrado.")


class LicenseResource(resources.ModelResource):
    status = fields.Field(
        attribute='status', 
        column_name='Status', 
        widget=widgets.CharWidget()
    )
    
    software = fields.Field(
        attribute='software', 
        column_name='Software', 
        widget=widgets.CharWidget()
    )
    
    license_type = fields.Field(
        column_name='Tipo de Licença',
        attribute='license_type',
        widget=ForeignKeyWidget(LicenseType, field='name')
    )

    assigned_to = fields.Field(
        column_name='Colaborador',
        attribute='assigned_to',
        widget=ForeignKeyWidget(Collaborator, field='name')
    )

    value = fields.Field(
        column_name='Valor',
        attribute='value'
    )

    description = fields.Field(
        column_name='Descrição',
        attribute='descripition'
    )

    purchase_date = fields.Field(
        column_name='Data de Compra',
        attribute='purchase_date'
    )

    expiration_date = fields.Field(
        column_name='Data de Expiração',
        attribute='expiration_date'
    )

    inventory_number = fields.Field(
        column_name='Nº de Inventário',
        attribute='inventory_number'
    )

    name = fields.Field(
        column_name='Nome',
        attribute='name',
    )

    license_key = fields.Field(
        column_name='Chave da Licença',
        attribute='license_key'
    )    

    class Meta:
        model = License
        fields = ('name', 'software', 'license_key', 'license_type', 'inventory_number', 'purchase_date', 'expiration_date', 'status', 'assigned_to', 'value', 'description')

    def dehydrate_status(self, license):
        return license.get_status_display()
    
    def dehydrate_software(self, license):
        return license.get_software_display()

    def before_import_row(self, row, **kwargs):
        status_map = {v: k for k, v in License.STATUS_CHOICES}
        if 'status' in row and row['status'] in status_map:
            row['status'] = status_map[row['status']]

        softwares_map= {v: k for k, v in License.SOFTWARE_CHOICES}
        if 'softwares' in row and row['softwares'] in softwares_map:
            row['softwares'] = softwares_map[row['softwares']]


def excel_date_to_date(excel_date):
    base_date = datetime(1899, 12, 30)
    return base_date + timedelta(days=excel_date)

class LicenseImportResource(resources.ModelResource):
    status = fields.Field(
        attribute='status', 
        column_name='status', 
        widget=widgets.CharWidget()
    )
    
    software = fields.Field(
        attribute='software', 
        column_name='software', 
        widget=widgets.CharWidget()
    )
    
    license_type = fields.Field(
        column_name='tipo_licenca',
        attribute='license_type',
        widget=ForeignKeyWidget(LicenseType, field='name')
    )

    assigned_to = fields.Field(
        column_name='colaborador',
        attribute='assigned_to',
        widget=ForeignKeyWidget(Collaborator, field='name')
    )

    value = fields.Field(
        column_name='valor',
        attribute='value'
    )

    description = fields.Field(
        column_name='descricao',
        attribute='description'
    )

    purchase_date = fields.Field(
        column_name='data_compra',
        attribute='purchase_date'
    )

    expiration_date = fields.Field(
        column_name='data_expiracao',
        attribute='expiration_date'
    )

    license_key = fields.Field(
        column_name='chave_licenca',
        attribute='license_key'
    )    

    class Meta:
        model = License
        fields = ('software', 'license_key', 'license_type', 'purchase_date', 'expiration_date', 'status', 'assigned_to', 'value', 'description')
        import_id_fields = ('license_key',)

    def dehydrate_status(self, license):
        return license.get_status_display()
    
    def dehydrate_software(self, license):
        return license.get_software_display()
    
    def before_import_row(self, row, **kwargs):
        status_map = {v: k for k, v in License.STATUS_CHOICES}
        if 'status' in row and row['status'] in status_map:
            row['status'] = status_map[row['status']]

        softwares_map= {v: k for k, v in License.SOFTWARE_CHOICES}
        if 'softwares' in row and row['softwares'] in softwares_map:
            row['softwares'] = softwares_map[row['softwares']]

        license_key = row.get('chave_licenca')
        if license_key and License.objects.filter(license_key=license_key).exists():
            raise ValidationError(f"A chave da licença '{license_key}' já está cadastrada.")
        
        if not row.get('data_compra'):
            row['data_compra'] = None
        if not row.get('data_expiracao'):
            row['data_expiracao'] = None

        for field in ['data_compra', 'data_expiracao']:
            if field in row and row[field]:
                try:
                    if isinstance(row[field], int) or isinstance(row[field], float):
                        row[field] = excel_date_to_date(row[field]).date()
                    else:
                        row[field] = datetime.strptime(row[field], '%Y-%m-%d').date()
                except Exception as e:
                    raise ValidationError(f"Erro ao processar o campo '{field}': {e}")
            else:
                row[field] = None

class PrinterResource(resources.ModelResource):
    status = fields.Field(
        column_name='Status',
        attribute='status',
        widget=widgets.CharWidget()
    )

    brand = fields.Field(
        column_name='Fabricante',
        attribute='brand',
        widget=ForeignKeyWidget(Brand, field='name')
    )

    category = fields.Field(
        column_name='Categoria',
        attribute='category',
        widget=ForeignKeyWidget(Category, field='name')
    )

    location = fields.Field(
        column_name='Localização',
        attribute='location',
        widget=ForeignKeyWidget(Sector, field='name')
    )

    name = fields.Field(
        column_name='Nome',
        attribute='name',
    )

    model = fields.Field(
        column_name='Modelo',
        attribute='model'
    )

    inventory_number = fields.Field(
        column_name='Nº de Inventário',
        attribute='inventory_number'
    )

    serie_number = fields.Field(
        column_name='Nº de Série',
        attribute='serie_number'
    )

    address = fields.Field(
        column_name='Endereço IP',
        attribute='address'
    )

    value = fields.Field(
        column_name='Valor',
        attribute='value'
    )

    description = fields.Field(
        column_name='Descrição',
        attribute='descripition'
    )

    class Meta:
        model = Printer
        fields = ('name', 'model', 'inventory_number', 'brand', 'category', 'serie_number', 'status', 'location', 'address', 'value', 'description')
        import_id_fields = ('serie_number',)

    def dehydrate_status(self, printer):
        return printer.get_status_display()

    def before_import_row(self, row, **kwargs):
        status_map = {v: k for k, v in Printer.STATUS_CHOICES}
        if 'status' in row and row['status'] in status_map:
            row['status'] = status_map[row['status']]

class PrinterImportResource(resources.ModelResource):
    status = fields.Field(
        attribute='status', 
        column_name='status', 
        widget=widgets.CharWidget()
    )

    brand = fields.Field(
        column_name='fabricante',
        attribute='brand',
        widget=ForeignKeyWidget(Brand, field='name')
    )

    category = fields.Field(
        column_name='categoria',
        attribute='category',
        widget=ForeignKeyWidget(Category, field='name')
    )

    location = fields.Field(
        column_name='localizacao',
        attribute='location',
        widget=ForeignKeyWidget(Sector, field='name')
    )

    model = fields.Field(
        column_name='modelo',
        attribute='model'
    )

    serie_number = fields.Field(
        column_name='numero_serie',
        attribute='serie_number'
    )

    address = fields.Field(
        column_name='endereco_ip',
        attribute='address'
    )

    value = fields.Field(
        column_name='valor',
        attribute='value'
    )

    description = fields.Field(
        column_name='descricao',
        attribute='descripition'
    )

    class Meta:
        model = Printer
        import_id_fields = ('serie_number',)
        fields = ('model', 'brand', 'category', 'serie_number', 'status', 'location', 'address', 'value', 'description')


    def dehydrate_status(self, printer):
        return printer.get_status_display()

    def before_import_row(self, row, **kwargs):
        status_map = {v: k for k, v in Printer.STATUS_CHOICES}
        if 'status' in row and row['status'] in status_map:
            row['status'] = status_map[row['status']]

        serie_number = row.get('numero_serie')
        if serie_number and Printer.objects.filter(serie_number=serie_number).exists():
            raise ValidationError(f"O número de série '{serie_number}' já está cadastrado.")