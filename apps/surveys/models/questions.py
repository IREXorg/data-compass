import uuid

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import TimeStampedModel


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
