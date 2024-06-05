from django import template

register = template.Library()


@register.filter
def format_price(price):
    formatted_price = f'{price:,.0f}'.replace(',', ' ')
    return formatted_price
