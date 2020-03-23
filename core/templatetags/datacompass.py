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


@register.filter
@stringfilter
def alert_class(value):
    """
    Returns a arert class based on the value.

    The alert classes are based on Bootstrap 4 alerts.
    """
    # using simple lookup table
    lookup = {
        'error': 'danger',
    }

    return lookup.get(value, value)


@register.filter
def lookup(value, key):
    if value:
        return value.get(key, None)
