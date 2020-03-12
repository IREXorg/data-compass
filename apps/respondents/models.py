import uuid

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import TimeStampedModel

from .managers import RespondentManager


class Respondent(TimeStampedModel):
    """
    A survey respondent.

    Authenticated respondents are linked to respective :attr:`~user` objects.
    For respondents linked to user, empty :attr:`~first_name`,
    :attr:`~last_name`, :attr:`~email` and :attr:`~gender` will
    be autopopulated from the user object when object :meth:`~save` method is called.
    """
    NOT_STARTED = 'not started'
    IN_PROGRESS = 'in progress'
    COMPLETED = 'completed'

    STATUS_CHOICES = (
        (NOT_STARTED, _('not yet started')),
        (IN_PROGRESS, _('started but not completed')),
        (COMPLETED, _('completed')),
    )

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
        ordering = ['-created_at']

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
        except self.responses.model.DoesNotExist:
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
