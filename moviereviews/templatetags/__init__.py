from django import template

register = template.Library()

@register.filter
def format_rating(value):
    """Format rating to one decimal place"""
    return f"{float(value):.1f}" if value else "0.0"

@register.filter
def stars(value):
    """Convert numeric rating to star display"""
    full = int(value)
    half = 1 if (value - full) >= 0.5 else 0
    empty = 5 - full - half
    return {
        'full': range(full),
        'half': half,
        'empty': range(empty)
    }