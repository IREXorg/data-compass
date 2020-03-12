from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy as reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from apps.projects.models import Project
from core.mixins import PageTitleMixin

from ..filters import SurveyListFilter
from ..forms import (SurveyCreateForm, SurveyEditStepFiveForm, SurveyEditStepFourForm, SurveyEditStepOneForm,
                     SurveyEditStepSixForm, SurveyEditStepThreeForm, SurveyEditStepTwoForm, SurveyUpdateForm)
from ..mixins import SurveyCreatorMixin, SurveyDetailMixin
from ..models import Survey


class SurveyListView(LoginRequiredMixin, PageTitleMixin, ListView):
    """
    List surveys view.

    Allow current signin user to view list of allowed surveys.

    **Example request**:

    .. code-block::

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

    .. code-block::

        POST  /surveys/create

    **Example request**:

    .. code-block::

        POST  /projects/1234567890/create-survey
    """

    # Translators: This is survey create page title
    page_title = _('Create a survey')
    template_name = 'surveys/survey_create.html'
    context_object_name = 'survey'
    model = Survey
    form_class = SurveyCreateForm

    def get_project(self):
        """
        Get project to associate a survey with from url parameters
        """
        project_pk = self.kwargs.get('project', None)
        if project_pk:
            return Project.objects.get(pk=project_pk)

    def get_form_kwargs(self):
        """
        Add project to form class initialization arguments
        """
        form_kwargs = super().get_form_kwargs()
        project = self.get_project()
        if project:
            form_kwargs['project'] = self.get_project()
        return form_kwargs

    def get_context_data(self, **kwargs):
        """
        Add project to view context data
        """
        context = super().get_context_data(**kwargs)
        project = self.get_project()
        if project:
            context['project'] = self.get_project()
        return context

    def get_success_url(self):
        return reverse('projects:project-detail', kwargs={'pk': self.object.project.pk})


class SurveyDetailView(LoginRequiredMixin, PageTitleMixin, DetailView):
    """
    View survey details view.

    Allow current signin user to view survey details.

    **Example request**:

    .. code-block::

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

    .. code-block::

        DELETE  /surveys/1234567890/delete
    """

    # Translators: This is survey delete page title
    page_title = _('Delete a survey')
    template_name = 'surveys/survey_delete.html'
    context_object_name = 'survey'
    model = Survey

    def get_success_url(self):
        return reverse('projects:project-detail', kwargs={'pk': self.object.project.pk})


class SurveyEditStartView(LoginRequiredMixin, PageTitleMixin, DetailView):
    """
    View survey edit start view.

    Allow current signin user to start edit survey details.

    **Example request**:

    .. code-block::

        GET  /surveys/1234567890/edit-start
    """

    # Translators: This is survey view page title
    page_title = _('Edit new survey')
    template_name = 'surveys/survey_edit_start.html'
    context_object_name = 'survey'
    model = Survey


class SurveyEditStepOneView(LoginRequiredMixin, SurveyCreatorMixin, SurveyDetailMixin, PageTitleMixin, UpdateView):
    """
    Update survey step one view.

    Allow current signin user to update existing survey details and
    redirect to survey edit step two page.

    **Example request**:

    .. code-block::

        PUT  /surveys/1234567890/edit-step-one
    """

    # Translators: This is survey update page title
    page_title = _('Edit new survey')
    template_name = 'surveys/survey_edit_step_one.html'
    context_object_name = 'survey'
    model = Survey
    form_class = SurveyEditStepOneForm

    def get_success_url(self):
        return reverse('surveys:survey-edit-step-two', kwargs={'pk': self.object.pk})


class SurveyEditStepTwoView(LoginRequiredMixin, SurveyCreatorMixin, SurveyDetailMixin, PageTitleMixin, UpdateView):
    """
    Edit survey step two view.

    Allow current signin user to update existing survey details and
    redirect to survey edit step three page.

    **Example request**:

    .. code-block::

        PUT  /surveys/1234567890/edit-step-two
    """

    # Translators: This is survey update page title
    page_title = _('Edit new survey')
    template_name = 'surveys/survey_edit_step_two.html'
    context_object_name = 'survey'
    model = Survey
    form_class = SurveyEditStepTwoForm

    def get_success_url(self):
        return reverse('surveys:survey-edit-step-three', kwargs={'pk': self.object.pk})


class SurveyEditStepThreeView(LoginRequiredMixin, SurveyCreatorMixin, SurveyDetailMixin, PageTitleMixin, UpdateView):
    """
    Edit survey step three view.

    Allow current signin user to update existing survey details and
    redirect to survey edit step four page.

    **Example request**:

    .. code-block::

        PUT  /surveys/1234567890/edit-step-three
    """

    # Translators: This is survey update page title
    page_title = _('Edit new survey')
    template_name = 'surveys/survey_edit_step_three.html'
    context_object_name = 'survey'
    model = Survey
    form_class = SurveyEditStepThreeForm

    def get_success_url(self):
        return reverse('surveys:survey-edit-step-four', kwargs={'pk': self.object.pk})


class SurveyEditStepFourView(LoginRequiredMixin, SurveyCreatorMixin, SurveyDetailMixin, PageTitleMixin, UpdateView):
    """
    Edit survey step four view.

    Allow current signin user to update existing survey details and
    redirect to survey edit step five page.

    **Example request**:

    .. code-block::

        PUT  /surveys/1234567890/edit-step-four
    """

    # Translators: This is survey update page title
    page_title = _('Edit new survey')
    template_name = 'surveys/survey_edit_step_four.html'
    context_object_name = 'survey'
    model = Survey
    form_class = SurveyEditStepFourForm

    def get_success_url(self):
        return reverse('surveys:survey-edit-step-five', kwargs={'pk': self.object.pk})


class SurveyEditStepFiveView(LoginRequiredMixin, SurveyCreatorMixin, SurveyDetailMixin, PageTitleMixin, UpdateView):
    """
    Edit survey step five view.

    Allow current signin user to update existing survey details and
    redirect to survey edit step six page.

    **Example request**:

    .. code-block::

        PUT  /surveys/1234567890/edit-step-five
    """

    # Translators: This is survey update page title
    page_title = _('Edit new survey')
    template_name = 'surveys/survey_edit_step_five.html'
    context_object_name = 'survey'
    model = Survey
    form_class = SurveyEditStepFiveForm

    def get_success_url(self):
        return reverse('surveys:survey-edit-step-six', kwargs={'pk': self.object.pk})


class SurveyEditStepSixView(LoginRequiredMixin, SurveyCreatorMixin, SurveyDetailMixin, PageTitleMixin, UpdateView):
    """
    Edit survey step five view.

    Allow current signin user to update existing survey details and
    redirect to survey edit step six page.

    **Example request**:

    .. code-block::

        PUT  /surveys/1234567890/edit-step-six
    """

    # Translators: This is survey update page title
    page_title = _('Edit new survey')
    template_name = 'surveys/survey_edit_step_six.html'
    context_object_name = 'survey'
    model = Survey
    form_class = SurveyEditStepSixForm

    def get_success_url(self):
        return reverse('surveys:survey-edit-finish', kwargs={'pk': self.object.pk})


class SurveyEditFinishView(LoginRequiredMixin, PageTitleMixin, DetailView):
    """
    View survey edit start view.

    Allow current signin user to finish edit survey details.

    **Example request**:

    .. code-block::

        GET  /surveys/1234567890/edit-finish
    """

    # Translators: This is survey view page title
    page_title = _('Edit new survey')
    template_name = 'surveys/survey_edit_finish.html'
    context_object_name = 'survey'
    model = Survey
