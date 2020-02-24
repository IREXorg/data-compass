from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import FormView, UpdateView

from core.exceptions import NotAuthenticated
from core.mixins import PageTitleMixin

from ..forms import RespondentConsentForm, RespondentForm
from ..mixins import ConsentCheckMixin, RespondentSurveyMixin
from ..models import Respondent


class RespondentConsentView(PageTitleMixin, RespondentSurveyMixin, FormView):
    """
    Asks respondent for consent and saves consent data in user's session.

    If user is not authenicated and the survey requires login,
    user will be redirected to default ``LOGIN_URL``

    If user is a new respondent for the survey a new respondent
    object will be created.

    On successful consent user will be redirected to continue
    with the survey.
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
        return self.survey.display_name

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
    """
    Prompts respondents to update their basic data for the survey.

    if consent hasn't been provided yet, user will be redirected to consent page.
    """
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
        return self.survey.display_name

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
        return reverse('surveys:dataset-response-list-create', kwargs={'pk': self.survey_response.pk})