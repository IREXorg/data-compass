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
    """
    Project Dataflow Hierarchy model class

    Defines how data is flowing among different actors in survey context.

    Once added, survey will ask Respondent(s) what is his/her hierarchy.
    They will choose that hierarchy from a list of options provided by a survey.
    """

    #: Global unique identifier for a dataflow hierarchy.
    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    #: Project under which an dataflow hierarchy belongs to.
    project = models.ForeignKey(
        'projects.Project',
        blank=True,
        verbose_name=_('project'),
        on_delete=models.CASCADE,
        related_name='hierarchies',
        related_query_name='hierarchy'
    )

    #: Top dataflow hierarchy(parent) under which an dataflow hierarchy belongs to.
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_('parent')
    )

    #: Hierarchy level under which an dataflow hierarchy belongs to.
    hierarchy_level = models.ForeignKey(
        'surveys.HierarchyLevel',
        on_delete=models.CASCADE,
        null=True,  # TODO: should be False. Added temprarily for the sake of migrations
        related_name='hierarchies',
        related_query_name='hierarchy',
    )
    level_name = models.CharField(_('level name'), max_length=128)

    #: Human readable name of a dataflow hierarchy.
    name = models.CharField(_('name'), max_length=128)

    #: Human readable, brief details about a dataflow hierarchy.
    description = models.TextField(_('description'), blank=True)

    #: User who created(or owning) a dataflow hierarchy.
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
        """Returns string representation of a dataflow hierarchy"""
        return self.name

    def save(self, *args, **kwargs):
        if self.parent:
            self.project = self.parent.project
        super().save(*args, **kwargs)
