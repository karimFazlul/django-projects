from django import template
import locale
from decimal import Decimal

# custom filter
register = template.Library()
@register.filter(name='currency')
def currency(value):
    try:
        locale.setlocale(locale.LC_ALL,'en_US.UTF-8')
    except:
        locale.setlocale(locale.LC_ALL,'')
    value = float(value)
    loc = locale.localeconv()
    return locale.currency(value, loc['currency_symbol'], grouping=True)
    