# core/templatetags/math_filters.py
from django import template

register = template.Library()


@register.filter
def multiply(value, arg):
    """Multiply two numbers"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def divide(value, arg):
    """Divide two numbers"""
    try:
        if float(arg) == 0:
            return 0
        return float(value) / float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def subtract(value, arg):
    """Subtract arg from value"""
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def add_filter(value, arg):
    """Add two numbers (custom add filter)"""
    try:
        return float(value) + float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def percentage(value, total):
    """Calculate percentage"""
    try:
        if float(total) == 0:
            return 0
        return (float(value) / float(total)) * 100
    except (ValueError, TypeError):
        return 0


@register.filter
def membership_progress(points, level):
    """Calculate membership progress percentage"""
    try:
        points = float(points)

        if level == 'BRONZE':
            target = 2000
            current = min(points, target)
            return (current / target) * 100
        elif level == 'SILVER':
            if points < 2000:
                return 0
            target = 5000
            current = min(points, target) - 2000
            return (current / 3000) * 100
        elif level == 'GOLD':
            if points < 5000:
                return 0
            target = 10000
            current = min(points, target) - 5000
            return (current / 5000) * 100
        else:  # PLATINUM
            return 100

    except (ValueError, TypeError):
        return 0


@register.filter
def points_needed(points, level):
    """Calculate points needed for next level"""
    try:
        points = int(points)

        if level == 'BRONZE':
            return max(0, 2000 - points)
        elif level == 'SILVER':
            return max(0, 5000 - points)
        elif level == 'GOLD':
            return max(0, 10000 - points)
        else:  # PLATINUM
            return 0

    except (ValueError, TypeError):
        return 0


@register.filter
def next_level_name(level):
    """Get next membership level name"""
    level_map = {
        'BRONZE': 'SILVER',
        'SILVER': 'GOLD',
        'GOLD': 'PLATINUM',
        'PLATINUM': 'PLATINUM'
    }
    return level_map.get(level, 'PLATINUM')


@register.filter
def format_currency(value):
    """Format number as Indonesian currency"""
    try:
        value = float(value)
        if value == 0:
            return "Gratis"

        # Convert to integer if it's a whole number
        if value == int(value):
            value = int(value)

        # Format with thousand separators
        return f"Rp {value:,}".replace(",", ".")
    except (ValueError, TypeError):
        return "Rp 0"


@register.filter
def progress_color(percentage):
    """Get color class based on progress percentage"""
    try:
        percentage = float(percentage)
        if percentage >= 90:
            return "bg-green-500"
        elif percentage >= 70:
            return "bg-blue-500"
        elif percentage >= 50:
            return "bg-yellow-500"
        elif percentage >= 30:
            return "bg-orange-500"
        else:
            return "bg-red-500"
    except (ValueError, TypeError):
        return "bg-gray-500"