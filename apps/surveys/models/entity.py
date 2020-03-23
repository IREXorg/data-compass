import uuid

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import TimeStampedModel


class Entity(TimeStampedModel):
    """
    Survey Entity model class

    Defines people, organizations, or teams—any person or group who
    might have, receive, or share information in survey context.

    Once added, survey will ask Respondents which entities
    might have, receive, or share information. They will choose that entity
    from a list of options provided by a survey.
    """

    #: Global unique identifier for an entity.
    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    #: Survey under which an entity belongs to.
    survey = models.ForeignKey(
        'surveys.Survey',
        related_name='entities',
        related_query_name='entity',
        verbose_name=_('survey'),
        on_delete=models.CASCADE,
    )

    #: Hierarchy level under which an entity belongs to.
    hierarchy_level = models.ForeignKey(
        'surveys.HierarchyLevel',
        verbose_name=_('hierarchy level'),
        related_name='entities',
        related_query_name='entity',
        on_delete=models.CASCADE,
        null=True
    )

    #: Human readable name of an entity.
    name = models.CharField(_('name'), max_length=255)

    #: Human readable, brief details about an entity.
    description = models.TextField(_('description'), blank=True)

    #: User who created(or owning) an entity
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('creator'),
        blank=True,
        related_name='created_survey_entities',
        related_query_name='created_survey_entity',
        on_delete=models.CASCADE
    )

    #: Extra entity fields.
    extras = JSONField(_('extras'), blank=True, default=dict)

    class Meta:
        verbose_name = _('Entity')
        verbose_name_plural = _('Entities')
        ordering = ['id']

    def __str__(self):
        """Returns string representation of an entity"""
        return self.name
