from django import forms
from .models import License, LicenseType
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

class LicensesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6'),
                Column('software', css_class='col-md-6'),
            ),
            Row(
                Column('license_key', css_class='col-md-6'),
                Column('license_type', css_class='col-md-6'),
            ),
            Row(
                Column('purchase_date', css_class='col-md-4'),
                Column('expiration_date', css_class='col-md-4'),
                Column('value', css_class='col-md-4'),
            ),
            Row(
                Column('status', css_class='col-md-6'),
                Column('category', css_class='col-md-6'),
            ),
            Row(
                Column('assigned_to', css_class='col-md-6'),
                Column('inventory_number', css_class='col-md-6'),
            ),
            'description',
            Submit('submit', 'Salvar')
        )




    class Meta:
        model = License
        fields = ['name', 'software', 'license_key', 'license_type', 'category', 'purchase_date', 'expiration_date', 'status', 'inventory_number', 'assigned_to', 'value', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'software': forms.Select(attrs={'class': 'form-select'}),
            'license_key': forms.TextInput(attrs={'class': 'form-control'}),
            'license_type': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'purchase_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'inventory_number': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'expiration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'value': forms.TextInput(attrs={'class': 'form-control mask-money'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
        }

        labels = {
            'name': 'Nome',
            'software': 'Software',
            'license_key': 'Chave da licença',
            'license_type': 'Tipo de licença',
            'purchase_date': 'Data de compra',
            'category': 'Categoria',
            'expiration_date': 'Data de expiração',
            'status': 'Status',
            'inventory_number': 'Número de Inventário',
            'value': 'Valor da Licença',
            'assigned_to': 'Usuário associado',
            'description': 'Descrição',
        }

class LicenseTypeForm(forms.ModelForm):
    class Meta:
        model = LicenseType
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }