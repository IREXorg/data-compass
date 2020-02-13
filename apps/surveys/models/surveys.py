import uuid

from django.conf import settings
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.utils.text import slugify
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
    level_name = models.CharField(_('level name'), max_length=128, unique=True)
    name = models.CharField(_('name'), max_length=128, unique=True)
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


class Role(TimeStampedModel):
    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    name = models.CharField(_('name'), max_length=255)
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


class Survey(TimeStampedModel):
    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    project = models.ForeignKey(
        'projects.project',
        related_name='surveys',
        related_query_name='survey',
        verbose_name=_('project'),
        on_delete=models.CASCADE
    )
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    display_name = models.CharField(
        _('display name'),
        max_length=255,
        blank=True
    )
    research_question = models.CharField(_('research question'), max_length=255)
    languages = ArrayField(
        models.CharField(max_length=5),
        verbose_name=_('languages'),
        blank=True,
        default=list
    )
    code = models.SlugField(
        _('code'),
        blank=True,
        allow_unicode=True,
        unique=True
    )
    login_required = models.BooleanField(
        _('login required'),
        help_text=_('Do you want users to login before responding to the survey?'),
        blank=True,
        default=True
    )
    respondent_can_aggregate = models.BooleanField(
        _('respondent can aggregate'),
        help_text=_("Do you want repondents to see visualizations or aggregates of other users' responses?"),
        blank=True,
        default=True
    )
    respondent_can_invite = models.BooleanField(
        _('respondent can suggest others'),
        help_text=_('Do you want users to share email addresses of other potential respondents?'),
        blank=True,
        default=True
    )
    is_active = models.BooleanField(
        _('is active'),
        help_text=_('Is published'),
        blank=True,
        default=True
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('creator'),
        blank=True,
        related_name='created_surveys',
        related_query_name='created_survey',
        on_delete=models.CASCADE
    )
    extras = JSONField(_('extras'), blank=True, default=dict)

    class Meta:
        verbose_name = _('Survey')
        verbose_name_plural = _('Surveys')

    def __str__(self):
        return self.display_name

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = slugify(self.name[:50])
        if not self.display_name:
            self.display_name = self.name
        super().save(*args, **kwargs)


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
    topic = models.ForeignKey(
        'surveys.Topic',
        related_name='datasets',
        related_query_name='dataset',
        verbose_name=_('topic'),
        on_delete=models.CASCADE
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
    group = models.ForeignKey(
        'surveys.QuestionGroup',
        related_name='questions',
        related_query_name='question',
        verbose_name=_('group'),
        on_delete=models.CASCADE
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