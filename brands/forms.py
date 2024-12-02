from django import forms
from . import models

class BrandsForm(forms.ModelForm):

    class Meta:
        model = models.Brand
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
        }

        labels = {
            'name': 'Fabricante',
            'description': 'Descrição',
        }