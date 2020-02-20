from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, UpdateView

from dateutil.parser import ParserError as DateTimeParserError
from dateutil.parser import parse as parse_datetime

from core.exceptions import NotAuthenticated
from core.mixins import PageTitleMixin

from ..forms import DatasetSelectForm, RespondentConsentForm, RespondentForm
from ..models import Respondent
from ..models import Response as SurveyResponse
from ..models import Survey


class RespondentSurveyMixin:
    """
    Provides ability to retrive a Survey object for user as a respondent.
    """

    #: Survey field to be queried against
    survey_slug_field = 'pk'

    #: URL parameter to be used for to provide a survey lookup value
    survey_slug_url_kwarg = 'pk'

    def get_survey(self, queryset=None):
        """
        Return survey object from queryset.

        If the user is not authenicated and survey requires login,
        raise ``NotAuthenticated``.

        If invitation is required and user is not on respondent
        list or not authenticated raise ``PermissionDenied``
        """

        # get lookup parameters
        slug = self.kwargs.get(self.survey_slug_url_kwarg)
        if not slug:
            raise AttributeError(
                _(f'{self.__class__.__name__} view must be called with {self.survey_slug_url_kwarg}.')
            )

        # get survey object matching the query
        queryset = queryset or Survey.objects.active()
        try:
            survey = queryset.get(**{self.survey_slug_field: slug})
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
        """Check if user has consented.

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


class RespondentConsentView(PageTitleMixin, RespondentSurveyMixin, FormView):
    """Ask respondent for consent.

    If the user is not authenicated and survey requires login,
    redirect user to ``LOGIN_URL``
    """

    # Basing this on Survey model because at this point a user might be
    # unauthenticated or not assosiated with any respondent object.
    form_class = RespondentConsentForm
    template_name = 'surveys/respondent_consent.html'

    def dispatch(self, *args, **kwargs):
        """
        Sets survey object then continue with request processing.

        If ``NotAuthenticated`` exception was raised user will be
        redirected to ``LOGIN_URL``.
        """
        self.respondent = None

        self.survey = self.get_survey()
        try:
            self.validate_respondent_for_survey()
        except NotAuthenticated:
            return redirect_to_login(self.request.get_full_path())

        return super().dispatch(*args, **kwargs)

    def get_page_title(self):
        return f'{self.survey.display_name}'

    def get_success_url(self):
        return reverse('surveys:respondent-update', kwargs={'pk': self.respondent.pk})

    def form_valid(self, form):
        """Get or create Respondent and save consent details in session."""
        # get or create respondent
        respondent_lookup = self.get_respondent_lookup()
        self.respondent = self.survey.get_or_create_respondent(**respondent_lookup)[0]

        # store consent details
        session_surveys = self.request.session.get('surveys', {})
        session_surveys[str(self.survey.pk)] = {
            'consented_at': timezone.now().isoformat()
        }
        self.request.session['surveys'] = session_surveys
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['survey'] = self.survey
        return context

    def get_respondent_lookup(self):
        """
        Returns parameters which can be used to check if user
        is already saved as survey respondent.
        """
        user = self.request.user
        email = self.request.GET.get('email')
        if user and not email:
            email = user.email

        return {'user': user, 'email': email}


class RespondentUpdateView(PageTitleMixin, RespondentSurveyMixin, ConsentCheckMixin, UpdateView):
    """Respondent Update View."""
    model = Respondent
    form_class = RespondentForm
    context_object_name = 'respondent'
    template_name = 'surveys/respondent_update.html'

    def dispatch(self, *args, **kwargs):
        self.survey_response = None
        self.object = self.get_object()
        self.survey = self.get_survey()

        try:
            self.validate_respondent_for_survey()
        except NotAuthenticated:
            return redirect_to_login(self.request.get_full_path())

        self.consented_at = self.get_consent(respondent=self.object, survey=self.survey)
        # If respondent has not provided the consent redirect to consent page
        if not self.consented_at:
            return redirect(reverse('surveys:respondent-consent', kwargs={'pk': self.survey.pk}))

        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return self.model.objects.active().select_related('survey', 'survey__project')

    def get_object(self, queryset=None):
        # Check if self.object is already set to prevent unnecessary DB calls
        if hasattr(self, 'object'):
            return self.object
        else:
            return super().get_object(queryset)

    def get_survey(self):
        return self.object.survey

    def get_form_kwargs(self):
        """
        Add project to form class initialization arguments and return
        keyword arguments required to instantiate the form.

        https://docs.djangoproject.com/en/3.0/ref/class-based-views/mixins-editing/#django.views.generic.edit.FormMixin.get_form_kwargs
        """
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.survey.project
        return kwargs

    def get_page_title(self):
        return f'{self.survey.display_name}'

    def form_valid(self, form):
        """
        Update Respondent, get or create Response then redirect to response
        update page.
        """
        self.object = form.save()

        if self.request.user.is_authenticated:
            creator = self.request.user
        else:
            creator = None

        self.survey_response = self.object.get_or_create_response(
            creator=creator,
            consented_at=self.consented_at
        )[0]
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('surveys:dataset-select', kwargs={'pk': self.survey_response.pk})


class DatasetSelectView(PageTitleMixin, RespondentSurveyMixin, ConsentCheckMixin, FormView):
    """Dataset Selection View.

    Allows user to select datasets.
    """
    form_class = DatasetSelectForm

    #: Field to be queried against
    slug_field = 'pk'

    #: URL parameter to be used for to provide a lookup value
    slug_url_kwarg = 'pk'

    template_name = 'surveys/dataset_select.html'

    def dispatch(self, *args, **kwargs):
        self.survey_response = self.get_survey_response()
        self.survey = self.get_survey()
        self.respondent = self.survey_response.respondent

        try:
            self.validate_respondent_for_survey()
        except NotAuthenticated:
            return redirect_to_login(self.request.get_full_path())

        self.consented_at = self.get_consent(respondent=self.respondent, survey=self.survey)
        # If respondent has not provided the consent redirect to consent page
        if not self.consented_at:
            return redirect(reverse('surveys:respondent-consent', kwargs={'pk': self.survey.pk}))

        # If respondent has not provided hierarchy yet redirect to respondent update page
        if not self.respondent.hierarchy:
            return redirect(reverse('surveys:respondent-update', kwargs={'pk': self.respondent.pk}))

        return super().dispatch(*args, **kwargs)

    def get_survey_response(self):
        slug = self.kwargs.get(self.slug_url_kwarg)
        if not slug:
            raise AttributeError(
                _(f'{self.__class__.__name__} view must be called with {self.slug_url_kwarg}.')
            )

        queryset = SurveyResponse.objects.active().select_related('survey', 'respondent')
        try:
            survey_response = queryset.get(**{self.slug_field: slug})
        except SurveyResponse.DoesNotExist:
            raise Http404(_('Page not found.'))

        return survey_response

    def get_survey(self):
        return self.survey_response.survey

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['survey'] = self.survey
        kwargs['survey_response'] = self.survey_response
        return kwargs

    def get_page_title(self):
        return f'{self.survey.display_name}'

    def form_valid(self, form):
        self.survey_response.set_dataset_responses(form.cleaned_data['datasets'])
        return redirect(self.request.get_full_path())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['survey_response'] = self.survey_response
        return context
