from django.contrib.auth.views import redirect_to_login
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, UpdateView

from core.exceptions import NotAuthenticated
from core.mixins import PageMixin

from ..forms import DatasetResponseFrequencyForm, DatasetSelectForm
from ..mixins import ConsentCheckMixin, RespondentSurveyMixin
from ..models import DatasetResponse
from ..models import Response as SurveyResponse


class DatasetResponseListCreateView(PageMixin, RespondentSurveyMixin, ConsentCheckMixin, FormView):
    """
    Allows user to select datasets.

    Creates a list of DatasetResponse objects based on selected datasets.
    """
    form_class = DatasetSelectForm

    #: Field to be queried against
    lookup_field = 'pk'

    #: URL parameter to be used for to provide a lookup value
    lookup_url_kwarg = 'pk'

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
        lookup_value = self.kwargs.get(self.lookup_url_kwarg)
        if not lookup_value:
            raise AttributeError(
                _(f'{self.__class__.__name__} view must be called with {self.lookup_url_kwarg}.')
            )

        queryset = SurveyResponse.objects.active().select_related('survey', 'respondent')
        try:
            survey_response = queryset.get(**{self.lookup_field: lookup_value})
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
        return self.survey.display_name

    def form_valid(self, form):
        self.survey_response.set_dataset_responses(form.cleaned_data['datasets'])
        return redirect(self.get_success_url())

    def get_success_url(self):
        # get first dataset response by default ordering
        first_dr = self.survey_response.dataset_responses.first()
        return reverse('surveys:dataset-response-update-frequency', kwargs={'pk': first_dr.pk})

    def get_back_url_path(self):
        return reverse('surveys:respondent-update', kwargs={'pk': self.survey_response.respondent.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['survey_response'] = self.survey_response
        return context


class BaseDatasetResponseUpdateView(PageMixin, RespondentSurveyMixin, ConsentCheckMixin, UpdateView):
    """
    Allows respondents to update response corresponding to the dataset the survey.
    """

    model = DatasetResponse
    context_object_name = 'dataset_response'

    def get_queryset(self):
        return DatasetResponse.objects.select_related('response', 'response__survey', 'dataset')

    def get_object(self, queryset=None):
        # Check if self.object is already set to prevent unnecessary DB calls
        if hasattr(self, 'object'):
            return self.object
        else:
            return super().get_object(queryset)

    def dispatch(self, *args, **kwargs):
        self.object = self.get_object()
        self.survey = self.object.response.survey
        self.survey_response = self.object.response

        # Check if user is allowed to take the survey
        try:
            self.validate_respondent_for_survey()
        except NotAuthenticated:
            return redirect_to_login(self.request.get_full_path())

        # Check respondent's consent
        self.consented_at = self.get_consent(respondent=self.object, survey=self.survey)
        if not self.consented_at:
            return redirect(reverse('surveys:respondent-consent', kwargs={'pk': self.survey.pk}))

        return super().dispatch(*args, **kwargs)

    def get_page_title(self):
        return self.survey.display_name


class DatasetResponseUpdateFrequencyView(BaseDatasetResponseUpdateView):
    form_class = DatasetResponseFrequencyForm
    template_name = 'surveys/dataset_response_update_frequency.html'

    def get_back_url_path(self):
        if self.object.is_first_in_response():
            return reverse('surveys:dataset-response-list-create', kwargs={'pk': self.survey_response.pk})
        return super().get_back_url_path()

    def get_success_url(self):
        return self.request.get_full_path()
