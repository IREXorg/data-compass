import uuid

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey

from core.models import TimeStampedModel


class DataflowHierarchy(TimeStampedModel, MPTTModel):
    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    project = models.ForeignKey(
        'projects.Project',
        blank=True,
        verbose_name=_('project'),
        on_delete=models.CASCADE,
        related_name='hierarchies',
        related_query_name='hierarchy'
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_('parent')
    )
    level_name = models.CharField(_('level name'), max_length=128)
    name = models.CharField(_('name'), max_length=128)
    description = models.TextField(_('description'), blank=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('creator'),
        blank=True,
        related_name='created_dataflow_hierarchy',
        related_query_name='created_dataflow_hierarchies',
        on_delete=models.CASCADE
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = _('Dataflow Hierarchy')
        verbose_name_plural = _('Dataflow Hierarchies')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.parent:
            self.project = self.parent.project
        super().save(*args, **kwargs)


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
