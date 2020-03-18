import uuid

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.urls import reverse_lazy as reverse
from django.utils.translation import ugettext_lazy as _

from core.models import TimeStampedModel


class Topic(TimeStampedModel):
    """
    Survey Topic model class

    Defines data subject(s) that respondent(s) dealt with in survey context.

    Once added, survey will ask Respondents how they work with data about a
    specific topic. They will choose that topic from a drop-down list of
    options provided by a survey.
    """

    #: Global unique identifier for a survey.
    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    #: Survey under which a topic belongs to.
    survey = models.ForeignKey(
        'survey',
        related_name='topics',
        related_query_name='topic',
        verbose_name=_('survey'),
        on_delete=models.CASCADE
    )

    #: Human readable name of a topic.
    name = models.CharField(_('name'), max_length=255)

    #: Human readable, brief details about a topic.
    description = models.TextField(_('description'), blank=True)

    #: User who created(or owning) a topic
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('creator'),
        blank=True,
        related_name='created_survey_topics',
        related_query_name='created_survey_topic',
        on_delete=models.CASCADE
    )

    #: Extra topic fields.
    extras = JSONField(_('extras'), blank=True, default=dict)

    class Meta:
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')

    def __str__(self):
        """Returns string representation of a topic"""
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


class DatasetFrequency(TimeStampedModel):
    """How often a dataset can be producd, accessed or shared."""
    survey = models.ForeignKey(
        'surveys.Survey',
        related_name='dataset_frequencies',
        related_query_name='dataset_frequency',
        verbose_name=_('survey'),
        on_delete=models.CASCADE
    )
    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    name = models.CharField(_('frequency'), max_length=255)

    class Meta:
        verbose_name = _('Dataset frequency')
        verbose_name_plural = _('Dataset Frequencies')

    def __str__(self):
        return self.name


class DatasetStorage(TimeStampedModel):
    """How dataset can be stored"""
    survey = models.ForeignKey(
        'surveys.Survey',
        related_name='dataset_storages',
        related_query_name='dataset_storage',
        verbose_name=_('survey'),
        on_delete=models.CASCADE
    )
    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    name = models.CharField(_('name'), max_length=255)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('creator'),
        blank=True,
        null=True,  # TODO: remove this
        related_name='created_survey_dataset_storages',
        related_query_name='created_survey_dataset_storage',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _('Dataset Storage')
        verbose_name_plural = _('Dataset Storage')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Obtain dataset storage absolute url."""
        return reverse('surveys:survey-detail', kwargs={'pk': self.pk})


class DatasetAccess(TimeStampedModel):
    """How dataset can be accessible"""
    survey = models.ForeignKey(
        'surveys.Survey',
        related_name='dataset_access',
        related_query_name='dataset_access',
        verbose_name=_('survey'),
        on_delete=models.CASCADE
    )
    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    name = models.CharField(_('name'), max_length=255)

    class Meta:
        verbose_name = _('Dataset Access')
        verbose_name_plural = _('Dataset Access')

    def __str__(self):
        return self.name
