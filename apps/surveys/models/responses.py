import uuid

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import TimeStampedModel


class Respondent(TimeStampedModel):
    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    survey = models.ForeignKey(
        'surveys.Survey',
        related_name='respondents',
        related_query_name='respondent',
        verbose_name=_('survey'),
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
        blank=True,
        null=True,
        related_name='respondents',
        related_query_name='respondent',
        on_delete=models.CASCADE
    )
    hierarchy = models.ForeignKey(
        'surveys.DataflowHierarchy',
        verbose_name=_('hierarchy'),
        related_name='respondents',
        related_query_name='respondent',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('creator'),
        blank=True,
        related_name='created_respondents',
        related_query_name='created_respondent',
        on_delete=models.CASCADE
    )
    extras = JSONField(_('extras'), blank=True, default=dict)

    class Meta:
        verbose_name = _('Respondent')
        verbose_name_plural = _('Respondents')

    def __str__(self):
        return f'{self.first_name} {self.first_name}'

    def save(self, *args, **kwargs):
        self.autopopulate_from_user()
        super().save(*args, **kwargs)

    def autopopulate_from_user(self):
        """Autopopulate empty `first_name`, `last_name` and `email` from instance user.
        """
        if not self.user:
            return

        if not self.first_name:
            self.first_name = self.user.first_name
        if not self.last_name:
            self.last_name = self.user.last_name
        if not self.email:
            self.email = self.user.email


class Response(TimeStampedModel):
    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    survey = models.ForeignKey(
        'surveys.Survey',
        related_name='responses',
        related_query_name='response',
        verbose_name=_('survey'),
        on_delete=models.CASCADE
    )
    respondent = models.ForeignKey(
        'surveys.Respondent',
        verbose_name=_('respondent'),
        related_name='responses',
        related_query_name='response',
        on_delete=models.CASCADE
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('creator'),
        blank=True,
        related_name='created_responses',
        related_query_name='created_response',
        on_delete=models.CASCADE
    )
    extras = JSONField(_('extras'), blank=True, default=dict)

    class Meta:
        verbose_name = _('Response')
        verbose_name_plural = _('Responses')

    def __str__(self):
        return self.survey


class QuestionResponse(TimeStampedModel):
    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    response = models.ForeignKey(
        'surveys.Response',
        verbose_name=_('response'),
        related_name='question_responses',
        related_query_name='question_response',
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        'surveys.Question',
        related_name='responses',
        related_query_name='response',
        verbose_name=_('survey'),
        on_delete=models.CASCADE
    )
    data = JSONField(_('data'), blank=True, default=dict)
    extras = JSONField(_('extras'), blank=True, default=dict)

    class Meta:
        verbose_name = _('Question Response')
        verbose_name_plural = _('Question Responses')

    def __str__(self):
        return self.survey
