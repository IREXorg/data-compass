import uuid

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import TimeStampedModel


class Logo(TimeStampedModel):
    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    survey = models.ForeignKey(
        'survey',
        related_name='logos',
        related_query_name='logo',
        verbose_name=_('survey'),
        on_delete=models.CASCADE
    )
    name = models.CharField(_('name'), max_length=255)
    image = models.ImageField(
        _('image'),
        blank=True,
        null=True,
        upload_to='surveys/logos'
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('creator'),
        blank=True,
        related_name='created_survey_logos',
        related_query_name='created_survey_logo',
        on_delete=models.CASCADE
    )
    extras = JSONField(_('extras'), blank=True, default=dict)

    class Meta:
        verbose_name = _('Logo')
        verbose_name_plural = _('Logos')

    def __str__(self):
        return self.name
