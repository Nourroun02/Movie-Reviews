from django import template

register = template.Library()

@register.filter
def stars_display(rating):
    """Convert numeric rating to star components"""
    try:
        rating = float(rating)
        full = int(rating)
        half = 1 if (rating - full) >= 0.5 else 0
        empty = 5 - full - half
        return {
            'full': range(full),
            'half': half,
            'empty': range(empty),
            'numeric': f"{rating:.1f}"
        }
    except (ValueError, TypeError):
        return {
            'full': range(0),
            'half': 0,
            'empty': range(5),
            'numeric': "0.0"
        }