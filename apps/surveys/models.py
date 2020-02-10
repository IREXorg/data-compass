import uuid

from django.conf import settings
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from core.models import TimeStampedModel


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
    learning_enquiry = models.CharField(_('learning enquiry'), max_length=255)
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
