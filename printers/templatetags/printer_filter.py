from django import template

register = template.Library()

@register.filter
def format_money(value):
    try:
        value = float(value)
        return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return value
    
@register.filter
def filter_name(field):
    fields = {
        'name': 'Nome',
        'model': 'Modelo',
        'brand': 'Fabricante',
        'category': 'Categoria',
        'status': 'Status',
        'serie_number': 'Número de série',
        'value': 'Valor',
        'address': 'Endereço IP',
        'location': 'Localização',
    }
    return fields.get(field, field)