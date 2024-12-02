from django import forms
from . import models

class CategoriesForm(forms.ModelForm):

    class Meta:
        model = models.Category
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
        }

        labels = {
            'name': 'Categoria',
            'description': 'Descrição',
        }