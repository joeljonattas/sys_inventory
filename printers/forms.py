from django import forms
from .models import Printer
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

class PrintersForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6'),
                Column('model', css_class='col-md-6'),
            ),
            Row(
                Column('brand', css_class='col-md-6'),
                Column('category', css_class='col-md-6'),
            ),
            Row(
                Column('status', css_class='col-md-6'),
                Column('value', css_class='col-md-6')
            ),
            Row(
                Column('location', css_class='col-md-6'),
                Column('address', css_class='col-md-6'),
            ),
            Row(
                Column('serie_number', css_class='col-md-6'),
                Column('inventory_number', css_class='col-md-6'),
            ),
            'description',
            Submit('submit', 'Salvar')
        )

    class Meta:
        model = Printer
        fields = ['name', 'model', 'brand', 'category', 'serie_number', 'inventory_number', 'status', 'location', 'address', 'value', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'brand': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'serie_number': forms.TextInput(attrs={'class': 'form-control'}),
            'inventory_number': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'state': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'value': forms.TextInput(attrs={'class': 'form-control mask-money'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

        labels = {
            'name': 'Nome',
            'model': 'Modelo',
            'brand': 'Fabricante',
            'category': 'Categoria',
            'inventory_number': 'Número de Inventário',
            'serie_number': 'Número de série',
            'status': 'Status',
            'state': 'Condição da impressora',
            'location': 'Localização',
            'address': 'Endereço IP',
            'value': 'Valor',
            'description': 'Descrição',
        }

