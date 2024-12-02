from django import forms
from . import models
from .models import Sector
from computers.models import Computer
from phones.models import Phone, PhoneNumber
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

class CollaboratorsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        computers = kwargs.pop('computers', Computer.objects.all())
        phones = kwargs.pop('phones', Phone.objects.all())
        phone_numbers = kwargs.pop('phone_numbers', PhoneNumber.objects.all())
        super().__init__(*args, **kwargs)
        
        self.fields['computer'].queryset = computers
        self.fields['phone'].queryset = phones
        self.fields['phone_number'].queryset = phone_numbers

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6'),
                Column('email', css_class='col-md-6'),
            ),
            Row(
                Column('sector', css_class='col-md-6'),
                Column('computer', css_class='col-md-6'),
            ),
            Row(
                Column('phone', css_class='col-md-6'),
                Column('phone_number', css_class='col-md-6'),
            ),
            'description',
            Submit('submit', 'Salvar')
        )

    class Meta:
        model = models.Collaborator
        fields = ['name', 'email', 'sector', 'computer', 'phone', 'phone_number', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'mask': 'email'}),
            'sector': forms.Select(attrs={'class': 'form-select'}),
            'computer': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.Select(attrs={'class': 'form-select'}),
            'phone_number': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
        }

        labels = {
            'name': 'Nome',
            'email': 'E-mail',
            'sector': 'Setor',
            'computer': 'Computador',
            'phone': 'Telefone',
            'phone_number': 'Linha Telefônica',
            'description': 'Descrição',
        }


class SectorsForm(forms.ModelForm):

    class Meta:
        model = models.Sector
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
        }

        labels = {
            'name': 'Setor',
            'description': 'Descrição',
        }