from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy as reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from core.mixins import PageTitleMixin

from ..filters import SurveyListFilter
from ..forms import SurveyCreateForm, SurveyUpdateForm
from ..mixins import SurveyCreatorMixin
from ..models import Survey


class SurveyListView(LoginRequiredMixin, PageTitleMixin, ListView):
    """
    List surveys view.

    Allow current signin user to view list of allowed surveys.

    **Example request**:

    .. code-block:: http

        GET  /surveys/
    """

    # Translators: This is surveys list page title
    page_title = _('Surveys List')
    template_name = 'surveys/survey_list.html'
    context_object_name = 'surveys'
    list_view_name = 'surveys/survey_list.html'
    model = Survey
    filterset_class = SurveyListFilter
    queryset = Survey.objects.all()
    ordering = ['created_at']
    paginate_by = 10


class SurveyCreateView(LoginRequiredMixin, SurveyCreatorMixin, PageTitleMixin, CreateView):
    """
    Create survey view.

    Allow current signin user to create a new survey and
    redirect to project survey list page.

    **Example request**:

    .. code-block:: http

        POST  /surveys/create
    """

    # Translators: This is survey create page title
    page_title = _('Create a survey')
    template_name = 'surveys/survey_create.html'
    context_object_name = 'survey'
    model = Survey
    form_class = SurveyCreateForm

    def get_success_url(self):
        return reverse('projects:project-detail', kwargs={'pk': self.object.project.pk})


class SurveyDetailView(LoginRequiredMixin, PageTitleMixin, DetailView):
    """
    View survey details view.

    Allow current signin user to view survey details.

    **Example request**:

    .. code-block:: http

        GET  /surveys/1234567890
    """

    # Translators: This is survey view page title
    page_title = _('View Survey')
    template_name = 'surveys/survey_detail.html'
    context_object_name = 'survey'
    model = Survey


class SurveyUpdateView(LoginRequiredMixin, SurveyCreatorMixin, PageTitleMixin, UpdateView):
    """
    Update survey details view.

    Allow current signin user to update existing survey details and
    redirect to project survey list page.

    **Example request**:

    .. code-block::

        PUT  /surveys/1234567890/update
    """

    # Translators: This is survey update page title
    page_title = _('Update a survey')
    template_name = 'surveys/survey_update.html'
    context_object_name = 'survey'
    model = Survey
    form_class = SurveyUpdateForm

    def get_success_url(self):
        return reverse('projects:project-detail', kwargs={'pk': self.object.project.pk})


class SurveyDeleteView(LoginRequiredMixin, PageTitleMixin, DeleteView):
    """
    Delete survey details

    Allow current signin user to delete existing survey and
    redirect to project survey list page.

    **Example request**:

    .. code-block:: http

        DELETE  /surveys/1234567890/delete
    """

    # Translators: This is survey delete page title
    page_title = _('Delete a survey')
    template_name = 'surveys/survey_delete.html'
    context_object_name = 'survey'
    model = Survey

    def get_success_url(self):
        return reverse('projects:project-detail', kwargs={'pk': self.object.project.pk})
