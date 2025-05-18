from django import template

register = template.Library()

@register.filter
def get_range(value):
    """Convert a number to range"""
    try:
        return range(1, int(value) + 1)
    except (ValueError, TypeError):
        return range(0)

@register.filter
def endswith(value, arg):
    return value.endswith(arg)