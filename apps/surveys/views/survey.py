from django.urls import reverse_lazy as reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from core.mixins import PageTitleMixin

from ..forms import SurveyForm
from ..models import Survey


class SurveyListView(PageTitleMixin, ListView):
    """
    List surveys view.

    Allow current signin user to view list of allowed surveys.
    """

    # Translators: This is surveys list page title
    page_title = _('Surveys List')
    template_name = 'surveys/survey_list.html'
    model = Survey
    context_object_name = 'surveys'
    # filterset_class = SurveyFilter
    # queryset = Survey.objects.all() use model filter
    # ordering = ['-created_at']
    paginate_by = 20


class SurveyCreateView(PageTitleMixin, CreateView):
    """
    Create survey view.

    Allow current signin user to create a new survey and
    redirect to survey list page.
    """

    # Translators: This is survey create page title
    page_title = _('Create Survey')
    template_name = 'surveys/survey_create.html'
    model = Survey
    form_class = SurveyForm
    success_url = reverse('surveys:survey-list')


class SurveyDetailView(PageTitleMixin, DetailView):
    """
    View survey details view.

    Allow current signin user to view survey details.
    """

    # Translators: This is survey view page title
    page_title = _('View Survey')
    template_name = 'surveys/survey_detail.html'
    model = Survey


class SurveyUpdateView(PageTitleMixin, UpdateView):
    """
    Update survey details view.

    Allow current signin user to update existing survey details and
    redirect to survey list page.
    """

    # Translators: This is survey update page title
    page_title = _('Update Survey')
    template_name = 'surveys/survey_update.html'
    model = Survey
    form_class = SurveyForm
    success_url = reverse('surveys:survey-list')


class SurveyDeleteView(PageTitleMixin, DeleteView):
    """
    Delete survey details

    Allow current signin user to delete existing survey and
    redirect to survey list page.
    """

    # Translators: This is survey delete page title
    page_title = _('Delete Survey')
    template_name = 'surveys/survey_delete.html'
    model = Survey
    success_url = reverse('surveys:survey-list')
