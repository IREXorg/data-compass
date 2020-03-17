from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views import View
from django.views.generic import DetailView, UpdateView
from django.views.generic.detail import SingleObjectMixin

from django_filters.views import FilterView

from apps.surveys.mixins import FacilitatorMixin
from core.exceptions import NotAuthenticated
from core.mixins import CSVResponseMixin, PageMixin

from ..filters import SurveyResponseFilter
from ..forms import SurveyResponseCompleteForm
from ..mixins import ConsentCheckMixin, RespondentSurveyMixin
from ..models import SurveyResponse


class SurveyResponseListView(FacilitatorMixin, PageMixin, CSVResponseMixin, FilterView):
    """
    Listing survey responses as a facilitator.
    """

    # Translators: This is respondents list page title
    page_title = _('Manage responses')
    template_name = 'responses/survey_response_list.html'
    context_object_name = 'survey_responses'
    model = SurveyResponse
    filterset_class = SurveyResponseFilter
    ordering = ['-created_at']
    paginate_by = 30

    def get_queryset(self):
        return self.model.objects\
            .filter(survey__project__facilitators=self.request.user)\
            .select_related('respondent', 'survey', 'survey__project')\
            .with_status()

    def get_rows(self):
        yield ('id', 'respondent_email', 'respondent_id', 'survey', 'survey_id', 'project', 'project_id',
               'status', 'consented_at', 'completed_at')

        for obj in self.object_list:
            yield (obj.id, obj.respondent.email, obj.respondent_id,
                   obj.survey.name, obj.survey_id, obj.survey.project.name, obj.survey.project.id,
                   obj.status, obj.consented_at, obj.completed_at)

    def get_filename(self):
        return f'responses-{str(timezone.now().date())}.csv'

    def get_renderer(self):
        # When `format=csv` in URL query string return csv
        if self.request.GET.get('format') == 'csv':
            return 'csv'


class SurveyResponseResumeView(LoginRequiredMixin, PageMixin, SingleObjectMixin, View):
    """
    Redirect to respondents last stage of survey response if possible.

    If the resume point won't be found user will beredirected to
    respondent information update page.
    """
    model = SurveyResponse

    def get_queryset(self):
        return self.model.objects\
            .active()\
            .filter(
                completed_at__isnull=True,
                consented_at__isnull=False,
                respondent__user=self.request.user)\
            .select_related('respondent', 'survey')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        # check last response URL from state data
        _state = self.object.extras.get('_state', {})
        resume_path = _state.get('resume_path')

        if not resume_path:
            # if resume point not found redirect to respondent information update
            return redirect(
                reverse('respondents:respondent-update', kwargs={'pk': self.object.respondent.pk})
            )

        return redirect(resume_path)


class SurveyResponseCompleteView(PageMixin, RespondentSurveyMixin, ConsentCheckMixin, UpdateView):
    """
    Prompts respondents to complete survey.

    if consent hasn't been provided yet, user will be redirected to consent page.
    """
    model = SurveyResponse
    form_class = SurveyResponseCompleteForm
    context_object_name = 'survey_response'
    template_name = 'responses/survey_response_complete.html'

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
            return redirect(reverse('respondents:respondent-consent', kwargs={'survey': self.survey.pk}))

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
            return reverse('responses:dataset-response-update-received', kwargs={'pk': last_dataset_response.pk})

        return '#'


class SurveyResponseDetailView(LoginRequiredMixin, PageMixin, DetailView):
    template_name = 'responses/survey_response_detail.html'
    context_object_name = 'survey_response'
    model = SurveyResponse

    def get_queryset(self):
        return self.model.objects\
            .filter(respondent__user=self.request.user)\
            .select_related('survey', 'respondent', 'respondent__gender', 'respondent__hierarchy')\
            .prefetch_related(
                'dataset_responses',
                'dataset_responses__dataset',
                'dataset_responses__dataset_frequency',
                'dataset_responses__datasettopicreceived_set',
                'dataset_responses__datasettopicreceived_set__entity',
                'dataset_responses__datasettopicreceived_set__topic',
                'dataset_responses__datasettopicshared_set',
                'dataset_responses__datasettopicshared_set__entity',
                'dataset_responses__datasettopicshared_set__topic',
                'dataset_responses__topic_responses',
                'dataset_responses__topic_responses__topic',
                'dataset_responses__topic_responses__percieved_owner',
                'dataset_responses__topic_responses__storages',
                'dataset_responses__topic_responses__storages__storage',
                'dataset_responses__topic_responses__storages__access'
            )

    def get_page_title(self):
        return _('Survey Response: %(survey_name)s') % {'survey_name': self.object.survey.name}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['respondent'] = self.object.respondent
        return context
