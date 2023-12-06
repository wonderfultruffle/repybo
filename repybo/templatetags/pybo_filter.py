from django import template

register = template.Library()

@register.filter
def sub(value, args):
    return value - args