from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ResponsesConfig(AppConfig):
    name = 'apps.responses'
    verbose_name = _('Responses')
