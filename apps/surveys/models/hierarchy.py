import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey

from core.models import TimeStampedModel


class HierarchyLevel(TimeStampedModel, MPTTModel):
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
        related_name='hierarchy_levels',
        related_query_name='hierarchy_level'
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_('parent')
    )

    name = models.CharField(_('name'), max_length=128)
    description = models.TextField(_('description'), blank=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('creator'),
        blank=True,
        related_name='created_hierarchy_levels',
        related_query_name='created_hierarchy_level',
        on_delete=models.CASCADE
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = _('Hierarchy Level')
        verbose_name_plural = _('Hierarchy Levels')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.parent:
            self.project = self.parent.project
        super().save(*args, **kwargs)


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
    hierarchy_level = models.ForeignKey(
        'surveys.HierarchyLevel',
        on_delete=models.CASCADE,
        null=True,  # TODO: should be False. Added temprarily for the sake of migrations
        related_name='hierarchies',
        related_query_name='hierarchy',
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
