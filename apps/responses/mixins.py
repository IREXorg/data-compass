from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.utils.translation import ugettext_lazy as _

from dateutil.parser import ParserError as DateTimeParserError
from dateutil.parser import parse as parse_datetime

from apps.surveys.models import Survey
from core.exceptions import NotAuthenticated
from core.mixins import FacilitatorMixin


class ResponseFacilitatorMixin(FacilitatorMixin):
    """
    CBV mixin which makes sure user is a facilitator and limits response
    queryset to only objects where the user is among the respective
    project facilitators.
    """

    def get_queryset(self):
        """
        Returns queryset of responses where user is among facilitators.
        """
        return self.model.objects.filter(survey__project__facilitators=self.request.user)


class ConsentCheckMixin:

    def get_consent(self, respondent=None, survey=None):
        """
        Check if user has consented.
        Returns consent datetime if user has consented otherwise None.
        """

        respondent = respondent or self.respondent
        survey = survey or self.survey

        # Check session
        session_surveys = self.request.session.get('surveys', {})
        session_survey = session_surveys.get(str(survey.pk), {})
        _consented_at = session_survey.get('consented_at')
        if _consented_at:
            try:
                return parse_datetime(_consented_at)
            except DateTimeParserError:
                pass

        # Check pre existing responses
        latest_response = respondent.get_latest_response()
        if latest_response:
            return latest_response.consented_at

        return None


class RespondentSurveyMixin:
    """
    Provides ability to retrive a Survey object for user as a respondent.
    """

    #: Survey field to be queried against
    survey_lookup_field = 'pk'

    #: URL parameter to be used for to provide a survey lookup value
    survey_lookup_url_kwarg = 'survey'

    def get_survey(self, queryset=None):
        """
        Return survey object from queryset.

        If the user is not authenicated and survey requires login,
        raise ``NotAuthenticated``.

        If invitation is required and user is not on respondent
        list or not authenticated raise ``PermissionDenied``
        """

        # get lookup parameters
        slug = self.kwargs.get(self.survey_lookup_url_kwarg)
        if not slug:
            raise AttributeError(
                _(f'{self.__class__.__name__} view must be called with {self.survey_lookup_url_kwarg}.')
            )

        # get survey object matching the query
        queryset = queryset or Survey.objects.active()
        try:
            survey = queryset.get(**{self.survey_lookup_field: slug})
        except Survey.DoesNotExist:
            raise Http404(_('Page not found.'))

        return survey

    def validate_respondent_for_survey(self):
        """Ensure user is allowed to take the survey"""
        if hasattr(self, 'survey'):
            survey = self.survey
        else:
            survey = self.get_survey()

        if not self.request.user.is_authenticated and survey.login_required:
            raise NotAuthenticated

        if survey.invitation_required and (
                not self.request.user.is_authenticated
                or not survey.respondents.filter(user=self.request.user).exists()):
            raise PermissionDenied(_('You are not allowed to take this survey'))
