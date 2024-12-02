from django import template

register = template.Library()

@register.filter
def filter_name(field):
    fields = {
        'name': 'Nome',
        'email': 'E-mail',
        'sector': 'Setor',
        'computer': 'Computador',
        'phone': 'Telefone',
        'phone number': 'Linha Telefônica',
    }
    return fields.get(field, field)