import uuid

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import TimeStampedModel

from .entity import Entity


class Role(TimeStampedModel):
    """
    Survey Role model class

    Defines all possible role(s) of respondent(s) in survey context.

    Once added, survey will ask Respondent(s) what is his/her role.
    They will choose that role from a list of options provided by a survey.
    """

    #: Global unique identifier for a role.
    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    #: Survey under which a role belongs to.
    survey = models.ForeignKey(
        'survey',
        related_name='roles',
        related_query_name='role',
        verbose_name=_('survey'),
        on_delete=models.CASCADE,
        null=True,  # TODO: remove this.
    )

    #: Hierarchy level under which a role belongs to.
    hierarchy_level = models.ForeignKey(
        'surveys.HierarchyLevel',
        verbose_name=_('hierarchy level'),
        related_name='roles',
        related_query_name='role',
        on_delete=models.CASCADE,
        null=True,  # TODO: remove this.
    )

    #: Human readable name of a role.
    name = models.CharField(_('name'), max_length=255)

    #: Human readable, brief details about a role.
    description = models.TextField(_('description'), blank=True)

    #: User who created(or owning) a role
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('creator'),
        blank=True,
        related_name='created_survey_roles',
        related_query_name='created_survey_role',
        on_delete=models.CASCADE
    )

    #: Extra role fields.
    extras = JSONField(_('extras'), blank=True, default=dict)

    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')

    def __str__(self):
        """Returns string representation of a role"""
        return self.name

    def save(self, *args, **kwargs):

        # TODO: For some reasons it was suggested Roles should also be available
        # as entities. Therefore as a temprary fix we are also saving new roles
        # in  entity model.
        # Potentially a better solution could be combining Role and Entity modes
        # to a single model.

        created = not bool(self.pk)
        super().save(*args, **kwargs)

        if created:
            Entity(
                name=self.name,
                survey=self.survey,
                hierarchy_level=self.hierarchy_level,
                description=self.description,
                creator=self.creator,
                extras={'_source': 'role', 'role_id': self.pk}
            ).save()
