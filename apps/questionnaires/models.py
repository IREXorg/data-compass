import uuid

from django.conf import settings
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from core.models import TimeStampedModel


class Questionnaire(TimeStampedModel):
    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    organization = models.ForeignKey(
        'organizations.Organization',
        blank=True,
        null=True,
        related_name='organization_questionnaires',
        related_query_name='organization_questionnaire',
        verbose_name=_('organization'),
        on_delete=models.SET_NULL
    )
    project = models.ForeignKey(
        'projects.project',
        blank=True,
        null=True,
        related_name='project_questionnaires',
        related_query_name='project_questionnaire',
        verbose_name=_('project'),
        on_delete=models.SET_NULL
    )
    phase = models.IntegerField(_('phase'), blank=True)
    extras = JSONField(_('extras'), blank=True, default=dict)

    class Meta:
        verbose_name = _('Questionnaire')
        verbose_name_plural = _('Questionnaires')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = slugify(self.name[:50])
        super().save(*args, **kwargs)
