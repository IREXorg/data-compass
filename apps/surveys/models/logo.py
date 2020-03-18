import uuid

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import TimeStampedModel


class Logo(TimeStampedModel):
    """
    Survey Logo model class

    Defines additional footer images to be added in survey footer.

    Once added, Respondent(s) will see added logo images on the survey footer.
    """

    #: Global unique identifier for a logo.
    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    #: Survey under which a logo belongs to.
    survey = models.ForeignKey(
        'survey',
        related_name='logos',
        related_query_name='logo',
        verbose_name=_('survey'),
        on_delete=models.CASCADE
    )

    #: Human readable name(caption) of a logo.
    name = models.CharField(_('name'), max_length=255)

    #: Human visible image file of a logo.
    image = models.ImageField(
        _('image'),
        blank=True,
        null=True,
        upload_to='surveys/logos'
    )

    #: User who created(or owning) a logo
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('creator'),
        blank=True,
        related_name='created_survey_logos',
        related_query_name='created_survey_logo',
        on_delete=models.CASCADE
    )

    #: Extra logo fields.
    extras = JSONField(_('extras'), blank=True, default=dict)

    class Meta:
        verbose_name = _('Logo')
        verbose_name_plural = _('Logos')

    def __str__(self):
        """Returns string representation of a logo"""
        return self.name
