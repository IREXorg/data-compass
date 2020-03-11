from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.utils.translation import ugettext_lazy as _

from dateutil.parser import ParserError as DateTimeParserError
from dateutil.parser import parse as parse_datetime

from core.exceptions import NotAuthenticated
from core.mixins import PopupModelFormMixin

from .models import Survey


class CreatorMixin:
    """
    CBV mixin which puts the user from the request as creator in
    form instance if not exist.

    Note: Using this mixin requires `LoginRequiredMixin`.
    """
    def form_valid(self, form):
        if not form.instance.creator_id:
            form.instance.creator = self.request.user
        return super().form_valid(form)


class SurveyCreatorMixin:
    """
    CBV mixin which puts the user from the request as survey creator in
    form instance if not exist.

    Note: Using this mixin requires `LoginRequiredMixin`.
    """
    def form_valid(self, form):
        if not form.instance.creator_id:
            form.instance.creator = self.request.user
        return super().form_valid(form)


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


class SurveyDetailMixin:
    """
    CBV mixin which puts releated survey objects into context data.

    Note: Using this mixin requires `LoginRequiredMixin`.
    """
    def get_topics(self):
        """
        Get topics associated with the survey
        """
        if self.object:
            return self.object.topics.all()

    def get_datasets(self):
        """
        Get datasets associated with the survey
        """
        if self.object:
            return self.object.datasets.all()

    def get_dataset_storages(self):
        """
        Get dataset storages associated with the survey
        """
        if self.object:
            return self.object.dataset_storages.all()

    def get_entities(self):
        """
        Get entities associated with the survey
        """
        if self.object:
            return self.object.entities.all()

    def get_context_data(self, **kwargs):
        """
        Add survey releated objects context data
        """
        context = super().get_context_data(**kwargs)
        topics = self.get_topics()
        datasets = self.get_datasets()
        dataset_storages = self.get_dataset_storages()
        entities = self.get_entities()
        if topics:
            context['topics'] = topics
        if datasets:
            context['datasets'] = datasets
        if dataset_storages:
            context['dataset_storages'] = dataset_storages
        if entities:
            context['entities'] = entities
        return context


class BasePopupModelFormMixin(PopupModelFormMixin):

    def get_popup_response_data(self):
        return {
            'action': 'change_object',
            'value': str(self.object.pk),
            'obj': str(self.object),
            'new_value': str(self.object.pk),
        }
