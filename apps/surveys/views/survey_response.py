from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import UpdateView

from core.exceptions import NotAuthenticated
from core.mixins import PageMixin

from ..forms import SurveyResponseCompleteForm
from ..mixins import ConsentCheckMixin, RespondentSurveyMixin
from ..models import Response as SurveyResponse


class SurveyResponseCompleteView(PageMixin, RespondentSurveyMixin, ConsentCheckMixin, UpdateView):
    """
    Prompts respondents to complete survey.

    if consent hasn't been provided yet, user will be redirected to consent page.
    """
    model = SurveyResponse
    form_class = SurveyResponseCompleteForm
    context_object_name = 'survey_response'
    template_name = 'surveys/survey_response_complete.html'

    def dispatch(self, *args, **kwargs):
        self.object = self.get_object()
        self.survey = self.object.survey
        self.respondent = self.object.respondent

        # Check if user is allowed to take the survey
        try:
            self.validate_respondent_for_survey()
        except NotAuthenticated:
            return redirect_to_login(self.request.get_full_path())

        # Check respondent's consent
        self.consented_at = self.get_consent(survey=self.survey)
        if not self.consented_at:
            return redirect(reverse('surveys:respondent-consent', kwargs={'pk': self.survey.pk}))

        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return self.model.objects.active().select_related('survey', 'respondent')

    def get_object(self, queryset=None):
        # Check if self.object is already set to prevent unnecessary DB calls
        if hasattr(self, 'object'):
            return self.object
        else:
            return super().get_object(queryset)

    def get_survey(self):
        return self.object.survey

    def get_page_title(self):
        return self.survey.display_name

    def form_valid(self, form):
        """
        Set response completion time.
        """
        form.instance.completed_at = timezone.now()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('users:profile-detail')

    def get_back_url_path(self):
        last_dataset_response = self.object.dataset_responses.last()
        if last_dataset_response:
            return reverse('surveys:dataset-response-update-received', kwargs={'pk': last_dataset_response.pk})

        return '#'
