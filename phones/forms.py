from django import forms
from . import models
from .models import PhoneNumber, PhoneOperator
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from phonenumbers import format_number, PhoneNumberFormat


class PhonesForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        numbers = kwargs.pop('numbers', PhoneNumber.objects.all())
        super().__init__(*args, **kwargs)
        
        # Define os queryset filtrados para os campos de seleção
        self.fields['number'].queryset = numbers

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
            ),Row(
                Column('serie_number', css_class='col-md-4'),
                Column('number', css_class='col-md-4'),
                Column('inventory_number', css_class='col-md-4'),
            ),
            'description',
            Submit('submit', 'Salvar')
        )

    class Meta:
        model = models.Phone
        fields = ['name', 'model', 'brand', 'status', 'category', 'serie_number', 'number', 'inventory_number', 'value', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'brand': forms.Select(attrs={'class': 'form-select'}),
            'serie_number': forms.TextInput({'class': 'form-control'}),
            'number': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'state': forms.Select(attrs={'class': 'form-select'}),
            'inventory_number': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'value': forms.TextInput(attrs={'class': 'form-control mask-money'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

        labels = {
            'name': 'Nome',
            'model': 'Modelo',
            'brand': 'Fabricante',
            'serie_number': 'Número de série',
            'number': 'Linha telefônica',
            'status': 'Status', 
            'inventory_number': 'Número de Inventário',
            'category': 'Categoria',
            'value': 'Valor',
            'description': 'Observação',
        }


class PhonesLinesForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.number:
            self.fields['number'].initial = format_number(
                self.instance.number, PhoneNumberFormat.NATIONAL
            )

        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6'),
                Column('number', css_class='col-md-6'),
            ),
            Row(
                Column('operator', css_class='col-md-6'),
                Column('status', css_class='col-md-6'),
            ),
            Row(
                Column('inventory_number', css_class='col-md-6'),
                Column('value', css_class='col-md-6'),
            ),
            'description',
            Submit('submit', 'Salvar')
        )


    class Meta:
        model = models.PhoneNumber
        fields = ['name', 'number', 'operator', 'status', 'inventory_number', 'value', 'description',]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control mask-phone'}),
            'operator': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'value': forms.TextInput(attrs={'class': 'form-control mask-money'}),
            'inventory_number': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

        labels = {
            'name': 'Nome',
            'number': 'Número',
            'operator': 'Operadora',
            'status': 'Status',
            'inventory_number': 'Número de Inventário',
            'value': 'Valor',
            'description': 'Observação',
        }

class OperatorsForm(forms.ModelForm):

    class Meta:
        model = PhoneOperator
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
        }

        labels = {
            'name': 'Operadora',
            'description': 'Descrição',
        }