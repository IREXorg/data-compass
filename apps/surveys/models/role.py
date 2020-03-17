import uuid

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import TimeStampedModel


class Role(TimeStampedModel):
    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    name = models.CharField(_('name'), max_length=255)
    survey = models.ForeignKey(
        'survey',
        related_name='roles',
        related_query_name='role',
        verbose_name=_('survey'),
        on_delete=models.CASCADE,
        null=True,  # TODO: remove this.
    )
    hierarchy = models.ForeignKey(
        'surveys.DataflowHierarchy',
        verbose_name=_('hierarchy'),
        related_name='roles',
        related_query_name='role',
        on_delete=models.CASCADE
    )
    description = models.TextField(_('description'), blank=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('creator'),
        blank=True,
        related_name='created_survey_roles',
        related_query_name='created_survey_role',
        on_delete=models.CASCADE
    )
    extras = JSONField(_('extras'), blank=True, default=dict)

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')

    def __str__(self):
        return self.name
