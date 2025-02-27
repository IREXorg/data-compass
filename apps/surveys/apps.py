from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SurveysConfig(AppConfig):
    name = 'apps.surveys'
    verbose_name = _('Surveys')

    def ready(self):
        from . import signals  # noqa
