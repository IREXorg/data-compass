from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def bgclass(value):
    """
    Returns a background class based on the value.

    The backround classes are inspired by Bootstrap 4 background color scheme.
    """
    # using simple lookup table
    lookup = {
        'not started': 'dark',
        'in progress': 'primary',
        'completed': 'success',
    }

    return lookup.get(value, '')
