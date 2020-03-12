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


class Topic(TimeStampedModel):
    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    survey = models.ForeignKey(
        'survey',
        related_name='topics',
        related_query_name='topic',
        verbose_name=_('survey'),
        on_delete=models.CASCADE
    )
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('creator'),
        blank=True,
        related_name='created_survey_topics',
        related_query_name='created_survey_topic',
        on_delete=models.CASCADE
    )
    extras = JSONField(_('extras'), blank=True, default=dict)

    class Meta:
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')

    def __str__(self):
        return self.name


class Dataset(TimeStampedModel):
    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    survey = models.ForeignKey(
        'survey',
        related_name='datasets',
        related_query_name='dataset',
        verbose_name=_('survey'),
        on_delete=models.CASCADE
    )
    topics = models.ManyToManyField(
        'surveys.Topic',
        related_name='datasets',
        related_query_name='dataset',
        verbose_name=_('topics'),
        blank=True
    )
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('creator'),
        blank=True,
        related_name='created_survey_datasets',
        related_query_name='created_survey_dataset',
        on_delete=models.CASCADE
    )
    extras = JSONField(_('extras'), blank=True, default=dict)

    class Meta:
        verbose_name = _('Dataset')
        verbose_name_plural = _('Datasets')

    def __str__(self):
        return self.name


class QuestionGroup(TimeStampedModel):
    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    survey = models.ForeignKey(
        'surveys.Survey',
        related_name='question_groups',
        related_query_name='question_group',
        verbose_name=_('survey'),
        on_delete=models.CASCADE
    )
    name = models.CharField(_('name'), blank=True, max_length=255)
    group_number = models.IntegerField(_('group number'), blank=True, null=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('creator'),
        blank=True,
        related_name='created_question_groups',
        related_query_name='created_question_group',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _('Question Group')
        verbose_name_plural = _('Question Groups')
        unique_together = ['survey', 'group_number']

    def __str__(self):
        return self.name


class Question(TimeStampedModel):
    INTEGER = 'integer'
    DECIMAL = 'decimal'
    TEXT = 'text'
    SELECT_ONE = 'select_one'
    SELECT_MULTIPLE = 'select_multiple'
    DATE = 'date'
    TIME = 'time'
    DATETIME = 'dateTime'
    IMAGE = 'image'
    FILE = 'file'

    TYPE_CHOICES = (
        (INTEGER, _('integer')),
        (DECIMAL, _('decimal')),
        (TEXT, _('text')),
        (SELECT_ONE, _('select one')),
        (SELECT_MULTIPLE, _('select multiple')),
        (DATE, _('date')),
        (TIME, _('time')),
        (DATETIME, _('date & time')),
        (IMAGE, _('image')),
        (FILE, _('file'))
    )

    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    survey = models.ForeignKey(
        'surveys.Survey',
        related_name='questions',
        related_query_name='question',
        verbose_name=_('survey'),
        on_delete=models.CASCADE
    )
    group = models.ForeignKey(  # TODO: remove this.
        'surveys.QuestionGroup',
        related_name='questions',
        related_query_name='question',
        verbose_name=_('group'),
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    name = models.SlugField(_('field name'), blank=True)
    label = models.CharField(
        _('label'),
        max_length=255,
        help_text=_('this will be displayed to user'),
    )
    type = models.CharField(_('type'), max_length=50, choices=TYPE_CHOICES)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('creator'),
        blank=True,
        related_name='created_questions',
        related_query_name='created_question',
        on_delete=models.CASCADE
    )
    options = JSONField(_('options'), blank=True, default=dict)

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')
        unique_together = ['survey', 'name']

    def __str__(self):
        return self.label


class Choice(TimeStampedModel):
    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    question = models.ForeignKey(
        'surveys.Question',
        verbose_name=_('question'),
        related_name='choices',
        related_query_name='choice',
        on_delete=models.CASCADE
    )
    name = models.SlugField(_('choice value'), blank=True)
    label = models.CharField(
        _('label'),
        max_length=255,
        help_text=_('this will be displayed to user'),
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('creator'),
        blank=True,
        related_name='created_survey_choices',
        related_query_name='created_survey_choice',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _('Choice')
        verbose_name_plural = _('Choices')

    def __str__(self):
        return self.label


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
