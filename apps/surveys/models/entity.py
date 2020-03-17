import uuid

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import TimeStampedModel


class Entity(TimeStampedModel):
    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    project = models.ForeignKey(
        'projects.Project',
        verbose_name=_('project'),
        on_delete=models.CASCADE,
        related_name='entities',
        related_query_name='entity',
        null=True,  # TODO: remove this.
    )
    survey = models.ForeignKey(
        'surveys.Survey',
        related_name='entities',
        related_query_name='entity',
        verbose_name=_('survey'),
        on_delete=models.CASCADE,
        null=True,  # TODO: remove this.
    )
    name = models.CharField(_('name'), max_length=255)
    hierarchy = models.ForeignKey(
        'surveys.DataflowHierarchy',
        related_name='entities',
        related_query_name='entity',
        on_delete=models.CASCADE,
        null=True,
        verbose_name=_('hierarchy'),
    )
    description = models.TextField(_('description'), blank=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('creator'),
        blank=True,
        related_name='created_survey_entities',
        related_query_name='created_survey_entity',
        on_delete=models.CASCADE
    )
    extras = JSONField(_('extras'), blank=True, default=dict)

    class Meta:
        verbose_name = _('Entity')
        verbose_name_plural = _('Entities')

    def __str__(self):
        return self.name
