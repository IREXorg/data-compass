import uuid

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import PermissionDenied
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse_lazy as reverse
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from core.fields import ChoiceArrayField
from core.models import TimeStampedModel

from ..managers import SurveyManager


class Survey(TimeStampedModel):
    """
    Survey model class

    Defines set of unique questions, that respondent encounters when taking
    it, with the purpose to understand data flow hierarchies, data topics,
    data sets, data sharing entities, data storage mechanisms and
    data access permissions.

    If the survey has :attr:`~login_required` set to ``True`` only logged in
    users should be allowed to respond to the survey.

    If the survey has :attr:`~invitation_required` set to ``True`` only
    users only invited users should be allowed to respond to the survey.
    Currently this only registered users can be invitees by being pre-added
    to the respondent list but this will change in future.
    """
    YES_NO_CHOICES = (
        (True, _('Yes')),
        (False, _('No'))
    )

    #: Global unique identifier for a survey.
    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    #: Project under which a survey belongs to.
    project = models.ForeignKey(
        'projects.project',
        related_name='surveys',
        related_query_name='survey',
        verbose_name=_('project'),
        on_delete=models.CASCADE
    )

    #: User who created(or owning) a survey
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('creator'),
        blank=True,
        related_name='created_surveys',
        related_query_name='created_survey',
        on_delete=models.CASCADE
    )

    #: Internal used survey name.
    name = models.CharField(
        _('name'),
        max_length=255
    )

    #: Human readable, brief details about survey.
    description = models.TextField(
        _('description')
    )

    #: Human readable, survey alternative name for respondents.
    display_name = models.CharField(
        _('alternative name'),
        help_text=_('Use this optional field to provide the survey name as '
                    'Respondents will see it.'),
        max_length=255,
        blank=True
    )

    #: Accompanies survey research questions.
    research_question = models.CharField(
        _('research question'),
        help_text=_('Every Data Compass survey must have a specific research '
                    'question. What is yours?'),
        max_length=255
    )

    #: Survey languages for translations.
    languages = ChoiceArrayField(
        models.CharField(
            max_length=5,
            choices=settings.LANGUAGES,
            ),
        help_text=_('By default, all surveys have an English version. '
                    'If your survey will be in other languages, select or '
                    'add them here. You will provide translations later.'),
        verbose_name=_('languages'),
        blank=True,
        default=list
    )

    #: A slug for the survey.
    code = models.SlugField(
        _('code'),
        blank=True,
        allow_unicode=True
    )

    #: Flag whether respondents should not be linked with system hierachy levels.
    dont_link_hierarchy_levels = models.BooleanField(
        _('do not link respondents with system hierarchy levels'),
        help_text=_('This can be easier in some contexts, but will limit aggregate or comparative analyses.'),
        blank=True,
        default=False,
        choices=YES_NO_CHOICES
    )

    #: Flag whether respondents can add their own hierarchy level.
    allow_respondent_hierarchy_levels = models.BooleanField(
        _('allow respondent hierarchy levels'),
        help_text=_("Respondents will select from the List you provided "
                    "for each level. If they can't find theirs, they can "
                    "add their own?"),
        blank=True,
        default=False,
        choices=YES_NO_CHOICES
    )

    #: Flag whether respondents can add their own roles.
    allow_respondent_roles = models.BooleanField(
        _('allow respondent roles'),
        help_text=_('If Yes, respondents will be able to add their own roles.'),
        blank=True,
        default=False,
        choices=YES_NO_CHOICES
    )

    #: Flag whether survey respondents must login.
    login_required = models.BooleanField(
        _('login required'),
        help_text=_("If no, they won't be able to save and return to their "
                    "responses, or view previous responses."),
        blank=True,
        default=True,
        choices=YES_NO_CHOICES
    )

    #: Flag whether survey respondents must be envited.
    invitation_required = models.BooleanField(
        _('invitation required'),
        help_text=_("If no, anyone with the survey link can respond to it."),
        blank=True,
        default=True,
        choices=YES_NO_CHOICES
    )

    #: Flag wether respondent can see others responses.
    respondent_can_aggregate = models.BooleanField(
        _('respondent can aggregate'),
        help_text=_("'Yes', will update their networ visual with all users' "
                    "responses in realtime. 'No' will not."),
        blank=True,
        default=True,
        choices=YES_NO_CHOICES
    )

    #: Flag wether respondent can invite others.
    respondent_can_invite = models.BooleanField(
        _('respondent can suggest others'),
        help_text=_('If Yes, the survey will include question collecting '
                    'email address. Respondents are responsible for '
                    'ensuring consent.'),
        blank=True,
        default=True,
        choices=YES_NO_CHOICES
    )

    #: Flag whether respondents can add their own topics.
    allow_respondent_topics = models.BooleanField(
        _('allow respondent topics'),
        help_text=_('If Yes, respondents will be able to add their own topics.'),
        blank=True,
        default=False,
        choices=YES_NO_CHOICES
    )

    #: Number of topics respondent have to complete for a survey
    respondent_topic_number = models.PositiveSmallIntegerField(
        _('respondent topic number'),
        help_text=_('Up to 10 topics are allowed'),
        blank=False,
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    #: Flag whether respondents can add their own datasets.
    allow_respondent_datasets = models.BooleanField(
        _('allow respondent datasets'),
        help_text=_('If Yes, respondents will be able to add their own datasets. This is not recommended.'),
        blank=True,
        default=False,
        choices=YES_NO_CHOICES
    )

    #: Flag whether respondents can add their own entities.
    allow_respondent_entities = models.BooleanField(
        _('allow respondent entities'),
        help_text=_('If Yes, respondents will be able to add their own entities.'),
        blank=True,
        default=False,
        choices=YES_NO_CHOICES
    )

    #: Flag whether respondents can add their own storages.
    allow_respondent_storages = models.BooleanField(
        _('allow respondent storages'),
        help_text=_('If Yes, respondents will be able to add their own storages.'),
        blank=True,
        default=False,
        choices=YES_NO_CHOICES
    )

    #: Human readable, header(introductory information) of survey.
    introduction_text = models.TextField(
        _('introduction text'),
        help_text=_('What text do you want to appear when a respondent begins the survey?'),
        default=''
    )

    #: Human readable, footer(closing information) of survey.
    closing_text = models.TextField(
        _('closing text'),
        help_text=_('What text do you want to appear when a respondent ends the survey?'),
        default=''
    )

    #: Flag is survey is published.
    is_active = models.BooleanField(
        _('is active'),
        help_text=_('Is published'),
        blank=True,
        default=False
    )

    #: Gender used in various parts of the survey.
    #
    #: ``post_save`` signal is used to automatially add primary genders on new
    #: instances with no pre-assigned genders.
    #: Users (`facilitators`) could be allowed to add or remove primary genders
    #: on a survey but shouldn't be allowed to modify attributes
    #: of an individual primary gender.
    genders = models.ManyToManyField(
        'users.Gender',
        verbose_name=_('genders'),
        related_name='surveys',
        related_query_name='survey',
        blank=True,
    )

    #: Flag whether survey collect respondent(s) email address.
    allow_collect_email = models.BooleanField(
        _('collect email address'),
        default=True
    )

    #: Flag whether survey collect respondent(s) name.
    allow_collect_name = models.BooleanField(
        _('collect name'),
        default=True
    )

    #: Flag whether survey collect respondent(s) gender.
    allow_collect_gender = models.BooleanField(
        _('collect gender'),
        default=True
    )

    #: Extra survey fields.
    extras = JSONField(
        _('extras'),
        blank=True,
        default=dict
    )

    #: Default manager.
    objects = SurveyManager()

    class Meta:
        verbose_name = _('Survey')
        verbose_name_plural = _('Surveys')
        ordering = ['-created_at']

    def __str__(self):
        """Returns string representation of survey"""
        return self.display_name

    def save(self, *args, **kwargs):
        """Save the survey."""

        if not self.code:
            self.code = slugify(self.name[:50])
        if not self.display_name:
            self.display_name = self.name
        super().save(*args, **kwargs)

    def get_or_create_respondent(self, user=None, email=None):
        """
        Get or create respondent.

        Returns: (respondent, created). If a new respondent was created in
        the process the second value of the tuple (created) will be ``True``.
        """
        # if login/user is not required
        if not self.login_required:
            if user and user.is_authenticated:
                return self.respondents.get_or_create(user=user, survey=self)
            elif email:
                return self.respondents.get_or_create(email=email, survey=self)

            respondent = self.respondents.create(survey=self)
            return (respondent, True)

        # user is required
        if not user.is_authenticated:
            raise PermissionDenied(_('A user is required'))
        return self.respondents.get_or_create(user=user, survey=self)

    def available_for_respondent(self, respondent):
        """
        Checks if the survey is available for respondent.

        Args:
            respondent: :class:`.Respondent` object

        Returns:
            bool: True if survey can be taken by respondent otherwise False.
        """
        user = None
        if respondent:
            user = respondent.user

        if user is None and (self.login_required or self.invitation_required):
            return False

        if self.invitation_required and not self.respondents.filter(user=user).exists():
            return False

        # Make sure user is not AnonymousUser
        if user.is_authenticated:
            return True

        return False

    def get_absolute_url(self):
        """Obtain survey absolute url."""
        return reverse('surveys:survey-detail', kwargs={'pk': self.pk})

    # Derive survey name abbreviation
    @property
    def abbreviation(self):
        parts = []

        words = self.name.split(' ')
        for word in words:
            parts.append(str(word[0]))

        return ''.join(parts[:2])
