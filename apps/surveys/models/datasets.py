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
    specific topic. They will choose that topic from a list of
    options provided by a survey.
    """

    #: Global unique identifier for a topic.
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
    """
    Survey Dataset model class

    Defines kind of data that respondent(s) dealt with in survey context
    about each topic.

    Once added, Respondents will share how they use or share a specific
    kind of data about each topic. They will choose that dataset from
    a list of options provided by a survey.
    """

    #: Global unique identifier for a dataset.
    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    #: Survey under which a dataset belongs to.
    survey = models.ForeignKey(
        'survey',
        related_name='datasets',
        related_query_name='dataset',
        verbose_name=_('survey'),
        on_delete=models.CASCADE
    )

    #: Linked topic(s) which a dataset associated with.
    topics = models.ManyToManyField(
        'surveys.Topic',
        related_name='datasets',
        related_query_name='dataset',
        verbose_name=_('topics'),
        blank=True
    )

    #: Human readable name of a dataset.
    name = models.CharField(_('name'), max_length=255)

    #: Human readable, brief details about a dataset.
    description = models.TextField(_('description'), blank=True)

    #: User who created(or owning) a dataset
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('creator'),
        blank=True,
        related_name='created_survey_datasets',
        related_query_name='created_survey_dataset',
        on_delete=models.CASCADE
    )

    #: Extra dataset fields.
    extras = JSONField(_('extras'), blank=True, default=dict)

    class Meta:
        verbose_name = _('Dataset')
        verbose_name_plural = _('Datasets')

    def __str__(self):
        """Returns string representation of a dataset"""
        return self.name


class DatasetFrequency(TimeStampedModel):
    """
    Survey Dataset Frequency model class

    Defines how often a dataset can be produced, accessed or shared in
    survey context.

    Once added, Respondents will share how often they produce, access or
    share a specific dataset. They will choose that dataset frequency from
    a list of options provided by a survey.
    """

    #: Global unique identifier for a dataset frequency.
    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    #: Survey under which a dataset frequency belongs to.
    survey = models.ForeignKey(
        'surveys.Survey',
        related_name='dataset_frequencies',
        related_query_name='dataset_frequency',
        verbose_name=_('survey'),
        on_delete=models.CASCADE
    )

    #: Human readable name of a dataset frequency.
    name = models.CharField(_('frequency'), max_length=255)

    # TODO: add creator, extras etc.

    class Meta:
        verbose_name = _('Dataset frequency')
        verbose_name_plural = _('Dataset Frequencies')

    def __str__(self):
        """Returns string representation of a dataset frequency"""
        return self.name


class DatasetStorage(TimeStampedModel):
    """
    Survey Dataset Storage model class

    Defines where data can be stored(or kept) in survey context.
    This can either be an information system, cabinet etc.

    Once added, Respondents will share how often they store a
    specific dataset. They will choose that dataset frequency from
    a list of options provided by a survey.
    """

    #: Global unique identifier for a dataset storage.
    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    #: Survey under which a dataset storage belongs to.
    survey = models.ForeignKey(
        'surveys.Survey',
        related_name='dataset_storages',
        related_query_name='dataset_storage',
        verbose_name=_('survey'),
        on_delete=models.CASCADE
    )

    #: Human readable name of a dataset storage.
    name = models.CharField(_('name'), max_length=255)

    #: User who created(or owning) a dataset storage
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
        """Returns string representation of a dataset storage"""
        return self.name

    def get_absolute_url(self):
        """Obtain dataset storage absolute url."""
        # TODO remove if no use
        return reverse('surveys:survey-detail', kwargs={'pk': self.pk})


class DatasetAccess(TimeStampedModel):
    """
    Survey Dataset Access model class

    Defines how a dataset accessed(accessible) in survey context.

    Once added, Respondents will share how often they access
    a specific dataset. They will choose that dataset access from
    a list of options provided by a survey.
    """

    #: Global unique identifier for a dataset access.
    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    #: Survey under which a dataset access belongs to.
    survey = models.ForeignKey(
        'surveys.Survey',
        related_name='dataset_access',
        related_query_name='dataset_access',
        verbose_name=_('survey'),
        on_delete=models.CASCADE
    )

    #: Human readable name of a dataset access.
    name = models.CharField(_('name'), max_length=255)

    # TODO: add creator, extras etc.

    class Meta:
        verbose_name = _('Dataset Access')
        verbose_name_plural = _('Dataset Access')

    def __str__(self):
        """Returns string representation of a dataset access"""
        return self.name
