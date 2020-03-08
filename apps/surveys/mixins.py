from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.postgres.search import SearchVector
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.utils.translation import ugettext_lazy as _

from dateutil.parser import ParserError as DateTimeParserError
from dateutil.parser import parse as parse_datetime

from core.exceptions import NotAuthenticated

from .models import Survey


class SurveyCreatorMixin:
    """
    CBV mixin which puts the user from the request as survey creator in
    form instance if not exist.
    Note: Using this mixin requires `LoginRequiredMixin`.
    """
    def form_valid(self, form):
        if not form.instance.creator_id:
            form.instance.creator = self.request.user
        form.save()
        return super().form_valid(form)


class FacilitatorMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    CBV mixin which makes sure user is a facilitator.
    """

    def test_func(self):
        """
        Ensure user is a facilitator.

        Returns true if user is facilitator.
        """
        return self.request.user.is_facilitator


class RespondentSurveyMixin:
    """
    Provides ability to retrive a Survey object for user as a respondent.
    """

    #: Survey field to be queried against
    survey_lookup_field = 'pk'

    #: URL parameter to be used for to provide a survey lookup value
    survey_lookup_url_kwarg = 'pk'

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


class SearchVectorFilterMixin:
    """FilterSet Mixin for text seach using Postgresql full text search."""

    def filter_search_vector(self, queryset, name, value):
        # NOTE: Ideally this should have a DB Index to avoid performance issues
        # https://docs.djangoproject.com/en/3.0/ref/contrib/postgres/search/#performance

        if not value:
            return queryset

        return queryset.annotate(
            search_vector=SearchVector(*self.search_vector_fields)
        ).filter(search_vector=value)
