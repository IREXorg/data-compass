from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class RespondentsConfig(AppConfig):
    name = 'apps.respondents'
    verbose_name = _('Respondents')
