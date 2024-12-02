from django import forms
from . import models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

class ComputersForm(forms.ModelForm):

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
                Column('value', css_class='col-md-6'),
            ),
            Row(
                Column('cpu', css_class='col-md-4'),
                Column('memory_ram', css_class='col-md-4'),
                Column('storage', css_class='col-md-4'),
            ),
            Row(
                Column('serie_number', css_class='col-md-6'),
                Column('inventory_number', css_class='col-md-6'),
            ),
            'description',
            Submit('submit', 'Salvar')
        )

    class Meta:
        model = models.Computer
        fields = ['name', 'model', 'brand', 'category', 'status', 'inventory_number', 'serie_number', 'cpu', 'memory_ram', 'storage', 'value', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'brand': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'state': forms.Select(attrs={'class': 'form-select'}),
            'inventory_number': forms.TextInput(attrs={'class': 'form-control'}),
            'serie_number': forms.TextInput({'class': 'form-control'}),
            'cpu': forms.TextInput({'class': 'form-control'}),
            'memory_ram': forms.Select(attrs={'class': 'form-select'}),
            'storage': forms.Select(attrs={'class': 'form-select'}),
            'value': forms.TextInput(attrs={'class': 'form-control mask-money'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
        }

        labels = {
            'name': 'Nome',
            'model': 'Modelo',
            'brand': 'Fabricante',
            'category': 'Categoria',
            'status': 'Status',
            'state': 'Estado do Equipamento',
            'serie_number': 'Número de série',
            'inventory_number': 'Número de Inventário',
            'cpu': 'Processador',
            'memory_ram': 'Memória RAM',
            'storage': 'Armazenamento',
            'value': 'Valor do equipamento',
            'description': 'Observação',
        }

