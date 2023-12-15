import markdown

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def sub(value, args):
    return value - args

@register.filter
def mark(value):
    extends = ["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extends=extends))