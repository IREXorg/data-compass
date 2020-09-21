from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.utils.translation import gettext_lazy as _

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


@register.filter(name='naturaltext')
def naturalize_text(value):
    lookup = {
        'not started': _('not started'),
        'in progress': _('in progress'),
        'completed': _('completed')
    }
    return lookup.get(value, value)


@register.filter(name='untranslatedurl')
def untranslate_url(path):
    langs = [lang[0] for lang in settings.LANGUAGES]
    path_components = path.split('/')
    if path_components[1] in langs:
        del path_components[1]
    return '/'.join(path_components)
