import uuid

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import TimeStampedModel

from ..managers import RespondentManager, SurveyResponseManager
from .surveys import Dataset


class Entity(TimeStampedModel):
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
        related_name='entities',
        related_query_name='entity',
        null=True,  # TODO: remove this.
    )
    name = models.CharField(_('name'), max_length=255)
    hierarchy = models.ForeignKey(
        'surveys.DataflowHierarchy',
        related_name='entities',
        related_query_name='entity',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_('hierarchy'),
    )
    description = models.TextField(_('description'), blank=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('creator'),
        blank=True,
        related_name='created_survey_entities',
        related_query_name='created_survey_entity',
        on_delete=models.CASCADE
    )
    extras = JSONField(_('extras'), blank=True, default=dict)

    class Meta:
        verbose_name = _('Entity')
        verbose_name_plural = _('Entities')

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

    class Meta:
        verbose_name = _('Dataset Storage')
        verbose_name_plural = _('Dataset Storage')

    def __str__(self):
        return self.name


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


class DatasetTopicStorageAccess(TimeStampedModel):
    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    response = models.ForeignKey(
        'surveys.DatasetTopicResponse',
        on_delete=models.CASCADE,
        related_name='storages',
        related_query_name='storage',
        verbose_name=_('dataset topic storage')
    )
    storage = models.ForeignKey(
        'surveys.DatasetStorage',
        on_delete=models.CASCADE,
        related_name='dataset_topic_responses',
        related_query_name='dataset_topic_response',
        verbose_name=_('dataset storage')
    )
    access = models.ForeignKey(
        'surveys.DatasetAccess',
        on_delete=models.CASCADE,
        related_name='dataset_topic_responses',
        related_query_name='dataset_topic_response',
        verbose_name=_('dataset access')
    )

    class Meta:
        verbose_name = _('Dataset Response Storage Access')
        verbose_name_plural = _('Dataset Response Storage Access')

    def __str__(self):
        return f'{self.storage} - {self.access}'

    @property
    def dataset(self):
        """The dataset."""
        return self.dataset_response.dataset


class DatasetTopicShared(TimeStampedModel):
    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    dataset_response = models.ForeignKey(
        'surveys.DatasetResponse',
        on_delete=models.CASCADE,
        verbose_name=_('dataset response')
    )
    entity = models.ForeignKey(
        'surveys.Entity',
        on_delete=models.CASCADE,
        verbose_name=_('entity')
    )
    topic = models.ForeignKey(
        'surveys.Topic',
        on_delete=models.CASCADE,
        verbose_name=_('topic')
    )

    class Meta:
        verbose_name = _('Dataset Topic Shared')
        verbose_name_plural = _('Dataset Topics Shared')

    def __str__(self):
        return f'{self.entity} - {self.topic}'

    @property
    def dataset(self):
        """The dataset."""
        return self.dataset_response.dataset


class DatasetTopicReceived(TimeStampedModel):
    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    dataset_response = models.ForeignKey(
        'surveys.DatasetResponse',
        on_delete=models.CASCADE,
        verbose_name=_('dataset response')
    )
    entity = models.ForeignKey(
        'surveys.Entity',
        on_delete=models.CASCADE,
        verbose_name=_('entity')
    )
    topic = models.ForeignKey(
        'surveys.Topic',
        on_delete=models.CASCADE,
        verbose_name=_('topic')
    )

    class Meta:
        verbose_name = _('Dataset Topic Received')
        verbose_name_plural = _('Dataset Topics Received')

    def __str__(self):
        return f'{self.entity} - {self.topic}'

    @property
    def dataset(self):
        """The dataset."""
        return self.dataset_response.dataset


class Respondent(TimeStampedModel):
    """
    A survey respondent.

    Authenticated respondents are linked to respective :attr:`~user` objects.
    For respondents linked to user, empty :attr:`~first_name`,
    :attr:`~last_name`, :attr:`~email` and :attr:`~gender` will
    be autopopulated from the user object when object :meth:`~save` method is called.
    """

    #: Respondent's UUID.
    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    #: Respondent's survey.
    survey = models.ForeignKey(
        'surveys.Survey',
        related_name='respondents',
        related_query_name='respondent',
        verbose_name=_('survey'),
        on_delete=models.CASCADE
    )

    #: User object related to the respondent. Usually this is ``None`` for
    #: unauthenticated respondents.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('user'),
        blank=True,
        null=True,
        related_name='respondents',
        related_query_name='respondent',
        on_delete=models.CASCADE
    )

    #: Respondent's first name.
    first_name = models.CharField(_('first name'), max_length=30, blank=True)

    #: Respondent's gender.
    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    #: Respondent's email.
    email = models.EmailField(_('email address'), blank=True)

    #: Respondent's gender.
    gender = models.ForeignKey(
        'users.Gender',
        blank=True,
        null=True,
        related_name='respondents',
        related_query_name='respondent',
        on_delete=models.SET_NULL,
        verbose_name=_('gender')
    )

    #: Hierarchy of the respondent in data flow
    hierarchy = models.ForeignKey(
        'surveys.DataflowHierarchy',
        verbose_name=_('hierarchy'),
        related_name='respondents',
        related_query_name='respondent',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    #: The user that recorded the respondent.
    #:
    #: For unauthenticated respondent this will usually be ``None``,
    #: but may be used to store the enumerator.
    #:
    #: For authenticated respondents this is expected the creator will
    #: to be the same as :attr:`~user`.
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('creator'),
        null=True,
        blank=True,
        related_name='created_respondents',
        related_query_name='created_respondent',
        on_delete=models.CASCADE
    )

    #: Extra data
    extras = JSONField(_('extras'), blank=True, default=dict)

    #:
    objects = RespondentManager()

    class Meta:
        verbose_name = _('Respondent')
        verbose_name_plural = _('Respondents')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        self.autopopulate_from_user()
        super().save(*args, **kwargs)

    def autopopulate_from_user(self):
        """Autopopulate empty  :attr:`~first_name`,
        :attr:`~last_name`, :attr:`~email` and :attr:`~gender`
        from the respective user.
        """
        if not self.user:
            return

        if not self.first_name:
            self.first_name = self.user.first_name
        if not self.last_name:
            self.last_name = self.user.last_name
        if not self.email:
            self.email = self.user.email
        if not self.gender:
            self.gender = self.user.gender

    def get_latest_response(self):
        """
        Get the latest response from the repondent.

        Returns `None` if no responden's response was found.
        """
        try:
            return self.responses.filter(survey=self.survey).latest('created_at')
        except Response.DoesNotExist:
            return None

    def get_or_create_response(self, creator=None, consented_at=None):
        """Get or Create Response object owned by the respondent."""
        response = self.get_latest_response()
        created = False

        if not response:
            response = self.responses.create(
                survey=self.survey,
                respondent=self,
                creator=creator,
                consented_at=consented_at
            )
            created = True

        if not created and response.consented_at != consented_at:
            response.consented_at = consented_at
            response.save()

        return (response, created)


class Response(TimeStampedModel):
    """A survey response.

    This glues all information received from the :class:`.Respondent` to a
    specific :class:`.Survey`. Other models holding partial survey response
    data are linked to this model.
    """

    #: Response UUID.
    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    #: Survey corresponding to the response.
    survey = models.ForeignKey(
        'surveys.Survey',
        related_name='responses',
        related_query_name='response',
        verbose_name=_('survey'),
        on_delete=models.CASCADE
    )

    #: The :class:`.Respondent` that provided the response.
    respondent = models.ForeignKey(
        'surveys.Respondent',
        verbose_name=_('respondent'),
        related_name='responses',
        related_query_name='response',
        on_delete=models.CASCADE
    )

    #: The user that created that recorded the response.
    #:
    #: For unauthenticated respondent this will usually be ``None``,
    #: but may be used to store the enumerator.
    #:
    #: For authenticated respondents this is expected the creator will
    #: to be the same as :attr:`.Respondent.user`.
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('creator'),
        null=True,
        blank=True,
        related_name='created_responses',
        related_query_name='created_response',
        on_delete=models.CASCADE
    )

    #: Date and Time when consent was received
    consented_at = models.DateTimeField(_('consented at'), blank=True, null=True)

    #: Date and time when the survey was completed.
    #: The value of this should be ``None`` for incomplete responses.
    completed_at = models.DateTimeField(_('completed at'), blank=True, null=True)

    #: Extra data.
    extras = JSONField(_('extras'), blank=True, default=dict)

    #: Default manager.
    objects = SurveyResponseManager()

    class Meta:
        verbose_name = _('Response')
        verbose_name_plural = _('Responses')

    def __str__(self):
        return f'{self.survey.display_name} response'

    def get_datasets(self, topic=False):
        """
        Get queryset of datasets associated with this response.

        Args:
            topic (bool): If topic is set to true the datasets will be
                queried based on DatasetTopicResponse model otherwise
                DatasetResponse model will be used.
        """
        if topic:
            return Dataset.objects.filter(response__topic_response=self)
        return Dataset.objects.filter(response__response=self)

    def set_dataset_responses(self, datasets):
        """Created or delete dataset responses according to the datasets."""

        # remove existing datasets responses according to the datasets.
        self.dataset_responses.exclude(dataset__in=datasets).delete()

        # get old dataset responses
        old_datasets = self.get_datasets()

        # add newly added datasets
        for dataset in datasets:
            if dataset not in old_datasets:
                self.dataset_responses.create(dataset=dataset)

        # set topic responses
        for dataset_response in self.dataset_responses.all():
            dataset_response.set_topic_responses()

    def set_resume_path(self, path):
        """Set resume URL path for the response."""
        _state = self.extras.get('_state', {})
        _state['resume_path'] = path
        self.extras['_state'] = _state
        self.__class__.objects.filter(id=self.id).update(extras=self.extras)


class DatasetResponse(TimeStampedModel):
    """A survey response related to a specific :class:`.Dataset`."""

    #: Dataset response UUID.
    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    #: The main survey :class:`.Response`.
    response = models.ForeignKey(
        'surveys.Response',
        verbose_name=_('response'),
        related_name='dataset_responses',
        related_query_name='dataset_response',
        on_delete=models.CASCADE
    )

    #: The dataset.
    dataset = models.ForeignKey(
        'surveys.Dataset',
        related_name='responses',
        related_query_name='response',
        verbose_name=_('dataset'),
        on_delete=models.CASCADE
    )
    #: Frequency of respondent producing, accessing or sharing the dataset.
    dataset_frequency = models.ForeignKey(
        'surveys.DatasetFrequency',
        null=True,
        blank=True,
        related_name='responses',
        related_query_name='response',
        on_delete=models.CASCADE,
        verbose_name=_('frequency')
    )

    #: Entities who respondents share those datasets with.
    shared_to = models.ManyToManyField(
        'surveys.Entity',
        related_name='dataset_responses_shared_to',
        related_query_name='dataset_response_shared_to',
        through='surveys.DatasetTopicShared',
        verbose_name=_('shared to')
    )

    #: Entities who respondents receive those datasets from.
    received_from = models.ManyToManyField(
        'surveys.Entity',
        related_name='dataset_responses_received_from',
        related_query_name='dataset_response_received_from',
        through='surveys.DatasetTopicReceived',
        verbose_name=_('received from')
    )

    # Extra data.
    extras = JSONField(_('extras'), blank=True, default=dict)

    class Meta:
        verbose_name = _('Dataset Response')
        verbose_name_plural = _('Dataset Responses')

    def __str__(self):
        return f'{self.survey.display_name} response'

    @property
    def respondent(self):
        """A survey respondent."""
        return self.response.respondent

    @property
    def survey(self):
        """The survey."""
        return self.response.survey

    def is_first_in_response(self):
        return not self.response.dataset_responses.filter(pk__lt=self.pk).exists()

    def is_last_in_response(self):
        return not self.response.dataset_responses.filter(pk__gt=self.pk).exists()

    def get_next_in_response(self):
        return self.response.dataset_responses.filter(pk__gt=self.pk).order_by('pk').first()

    def get_previous_in_response(self):
        return self.response.dataset_responses.filter(pk__lt=self.pk).order_by('-pk').first()

    def set_topic_responses(self):
        """Created or delete dataset-topic responses for the dataset."""

        # get dataset topics
        topics = self.dataset.topics.all() or self.survey.topics.all()

        # remove existing dataset-topic unwanted topic responses.
        self.topic_responses.exclude(topic__in=topics).delete()

        # get old topics
        old_topics = list(self.topic_responses.values_list('topic_id', flat=True))

        # add missing topic responses
        for topic in topics:
            if topic.id not in old_topics:
                self.topic_responses
                self.topic_responses.create(topic=topic)


class DatasetTopicResponse(TimeStampedModel):
    """A survey response related to a specific :class:`.Dataset`
    - :class:`.Topic` set."""

    #: Datatest topic response UUID.
    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    #: The dataset response object.
    dataset_response = models.ForeignKey(
        'surveys.DatasetResponse',
        verbose_name=_('dataset response'),
        related_name='topic_responses',
        related_query_name='topic_response',
        on_delete=models.CASCADE
    )

    #: The topic.
    topic = models.ForeignKey(
        'surveys.Topic',
        related_name='dataset_responses',
        related_query_name='dataset_response',
        verbose_name=_('topic'),
        on_delete=models.CASCADE
    )

    #: Entity perceived as owners of the dataset within the organization.
    percieved_owner = models.ForeignKey(
        'surveys.Role',
        related_name='percieved_owns_datasets',
        related_query_name='percieved_owns_dataset',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_('perceived owner')
    )

    #: Extra data.
    extras = JSONField(_('extras'), blank=True, default=dict)

    class Meta:
        verbose_name = _('Dataset Topic Response')
        verbose_name_plural = _('Dataset Topic Responses')

    def __str__(self):
        return self.survey.display_name

    @property
    def respondent(self):
        """A survey respondent."""
        return self.dataset_response.respondent

    @property
    def survey(self):
        """The survey."""
        return self.dataset_response.survey

    @property
    def dataset(self):
        """The dataset."""
        return self.dataset_response.dataset

    def is_first_in_response(self):
        return not self.dataset_response.topic_responses.filter(pk__lt=self.pk).exists()

    def is_last_in_response(self):
        return not self.dataset_response.topic_responses.filter(pk__gt=self.pk).exists()

    def get_next_in_response(self):
        return self.dataset_response.topic_responses.filter(pk__gt=self.pk).order_by('pk').first()

    def get_previous_in_response(self):
        return self.dataset_response.topic_responses.filter(pk__lt=self.pk).order_by('-pk').first()


class QuestionResponse(TimeStampedModel):
    """A survey response related to a specific :class:`.Question`.

    ..Note: This is model only holds data related to user-defined
        extra questions. It doesn't store response data related to
        all survey questions.
    """

    #: Question Response UUID
    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    #: The main survey response.
    response = models.ForeignKey(
        'surveys.Response',
        verbose_name=_('response'),
        related_name='question_responses',
        related_query_name='question_response',
        on_delete=models.CASCADE
    )

    #: The :class:`.Question` corresponding to this response.
    question = models.ForeignKey(
        'surveys.Question',
        related_name='responses',
        related_query_name='response',
        verbose_name=_('survey'),
        on_delete=models.CASCADE
    )

    #: Question response data
    data = JSONField(_('data'), blank=True, default=dict)

    #: Extra data
    extras = JSONField(_('extras'), blank=True, default=dict)

    class Meta:
        verbose_name = _('Question Response')
        verbose_name_plural = _('Question Responses')

    def __str__(self):
        return self.survey.display_name

    @property
    def respondent(self):
        """A survey respondent."""
        return self.response.respondent

    @property
    def survey(self):
        """The survey."""
        return self.response.survey
