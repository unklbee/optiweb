# Buat file baru: core/templatetags/math_filters.py

from django import template

register = template.Library()

@register.filter
def subtract(value, arg):
    """Subtracts the arg from the value."""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def multiply(value, arg):
    """Multiplies the value by the arg."""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def divide(value, arg):
    """Divides the value by the arg."""
    try:
        return int(value) / int(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

@register.filter
def percentage(value, total):
    """Calculate percentage: (value/total)*100"""
    try:
        if int(total) == 0:
            return 0
        return (int(value) * 100) / int(total)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0