from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy as reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from core.mixins import PageTitleMixin, SuccessMessageMixin

from ..filters import SurveyListFilter
from ..forms import (SurveyCreateForm, SurveyEditStepFiveForm, SurveyEditStepFourForm, SurveyEditStepOneForm,
                     SurveyEditStepSixForm, SurveyEditStepThreeForm, SurveyEditStepTwoForm, SurveyPublishForm,
                     SurveyUnpublishForm, SurveyUpdateForm)
from ..mixins import ProjectFacilitatorRequiredMixin, SurveyCreatorMixin, SurveyDetailMixin, SurveyFacilitatorMixin
from ..models import Survey


class SurveyListView(SurveyFacilitatorMixin, PageTitleMixin, ListView):
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


class SurveyCreateView(SuccessMessageMixin, ProjectFacilitatorRequiredMixin,
                       SurveyCreatorMixin, PageTitleMixin, CreateView):
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
    success_message = _('Survey was created successfully')

    def form_valid(self, form):
        """
        Add project to survey instance the save the survey.
        """
        form.instance.project = self.project
        return super().form_valid(form)

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
        return reverse('surveys:survey-detail', kwargs={'pk': self.object.pk})


class SurveyDetailView(SurveyFacilitatorMixin, PageTitleMixin, DetailView):
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


class SurveyUpdateView(SuccessMessageMixin, SurveyFacilitatorMixin,
                       SurveyCreatorMixin, PageTitleMixin, UpdateView):
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
    success_message = _('Survey was updated successfully')

    def get_success_url(self):
        return reverse('surveys:survey-detail', kwargs={'pk': self.object.pk})


class SurveyDeleteView(SuccessMessageMixin, SurveyFacilitatorMixin,
                       PageTitleMixin, DeleteView):
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
    success_message = _('Survey was deleted successfully')

    def get_success_url(self):
        return reverse('projects:project-detail', kwargs={'pk': self.object.project.pk})


class SurveyUnpublishView(SuccessMessageMixin, SurveyFacilitatorMixin,
                          PageTitleMixin, UpdateView):
    """
    Unpublish survey details

    Allow current signin user to unpublish existing survey and
    redirect to project survey list page.

    **Example request**:

    .. code-block::

        PUT  /surveys/1234567890/unpublish
    """

    # Translators: This is survey unpublish page title
    page_title = _('Unpublish a survey')
    template_name = 'surveys/survey_unpublish.html'
    context_object_name = 'survey'
    model = Survey
    form_class = SurveyUnpublishForm
    success_message = _('Survey was unpublished successfully')

    def form_valid(self, form):
        form.instance.is_active = False
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('surveys:survey-detail', kwargs={'pk': self.object.pk})


class SurveyPublishView(SuccessMessageMixin, SurveyFacilitatorMixin,
                        PageTitleMixin, UpdateView):
    """
    Publish survey details

    Allow current signin user to publish existing survey and
    redirect to project survey list page.

    **Example request**:

    .. code-block::

        PUT  /surveys/1234567890/publish
    """

    # Translators: This is survey publish page title
    page_title = _('Publish a survey')
    template_name = 'surveys/survey_publish.html'
    context_object_name = 'survey'
    model = Survey
    form_class = SurveyPublishForm
    success_message = _('Survey was published successfully')

    def get_success_url(self):
        return reverse('surveys:survey-detail', kwargs={'pk': self.object.pk})

    def show_error_message(self, message):
        # notify why survey publish was not successful
        messages.error(self.request, message)

    def form_valid(self, form):
        # Ensure survey has respondents before publishing
        respondents_count = self.object.respondents.count()
        if not respondents_count or respondents_count == 0:
            message = _('Failed to publish a survey. '
                        'Respondents are missing. Please add respondents to a survey.')
            self.show_error_message(message)
            to_url = '{}#id_respondents'.format(reverse('surveys:survey-edit-step-one', kwargs={'pk': self.object.pk}))
            return redirect(to_url)

        # Ensure survey has roles before publishing
        roles_count = self.object.roles.count()
        if not roles_count or roles_count == 0:
            message = _('Failed to publish a survey. '
                        'Roles are missing. Please add roles to a survey.')
            self.show_error_message(message)
            to_url = '{}#id_roles'.format(reverse('surveys:survey-edit-step-one', kwargs={'pk': self.object.pk}))
            return redirect(to_url)

        # Ensure survey has topics before publishing
        topics_count = self.object.datasets.count()  # TODO: restore to Topic
        if not topics_count or topics_count == 0:
            message = _('Failed to publish a survey. '
                        'Topics are missing. Please add topics to a survey.')
            self.show_error_message(message)
            to_url = '{}#id_topics'.format(reverse('surveys:survey-edit-step-two', kwargs={'pk': self.object.pk}))
            return redirect(to_url)

        # Ensure survey has datasets before publishing
        datasets_count = self.object.topics.count()  # TODO: restore to Dataset
        if not datasets_count or datasets_count == 0:
            message = _('Failed to publish a survey. '
                        'Datasets are missing. Please add datasets to a survey.')
            self.show_error_message(message)
            to_url = '{}#id_datasets'.format(reverse('surveys:survey-edit-step-three', kwargs={'pk': self.object.pk}))
            return redirect(to_url)

        # Ensure survey has entities before publishing
        entities_count = self.object.entities.count()
        if not entities_count or entities_count == 0:
            message = _('Failed to publish a survey. '
                        'Entities are missing. Please add entities to a survey.')
            self.show_error_message(message)
            to_url = '{}#id_entities'.format(reverse('surveys:survey-edit-step-four', kwargs={'pk': self.object.pk}))
            return redirect(to_url)

        # Ensure survey has dataset storages before publishing
        dataset_storages_count = self.object.dataset_storages.count()
        if not dataset_storages_count or dataset_storages_count == 0:
            message = _('Failed to publish a survey. '
                        'Dataset storages are missing. '
                        'Please add dataset storages to a survey.')
            self.show_error_message(message)
            to_url = '{}#id_dataset_storages'.format(
                reverse('surveys:survey-edit-step-five', kwargs={'pk': self.object.pk})
            )
            return redirect(to_url)

        # Ensure survey has genders before publishing
        genders_count = self.object.genders.count()
        if not genders_count or genders_count == 0:
            message = _('Failed to publish a survey. '
                        'Genders are missing. Please add genders to a survey.')
            self.show_error_message(message)
            to_url = '{}#id_genders'.format(reverse('surveys:survey-edit-step-six', kwargs={'pk': self.object.pk}))
            return redirect(to_url)

        # publish survey
        form.instance.is_active = True
        return super().form_valid(form)


class SurveyShareView(SurveyFacilitatorMixin, PageTitleMixin, DetailView):
    """
    Share survey view.

    Allow current signin user to share survey ling.

    **Example request**:

    .. code-block::

        GET  /surveys/1234567890/share
    """

    # Translators: This is survey share page title
    page_title = _('Share Survey')
    template_name = 'surveys/survey_share.html'
    context_object_name = 'survey'
    model = Survey

    def get_page_title(self):
        return _('Share') + ' ' + self.object.name


class SurveyEditStartView(SurveyFacilitatorMixin, PageTitleMixin, DetailView):
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

    def get_page_title(self):
        return _('Edit') + ' ' + self.object.name


class SurveyEditStepOneView(SuccessMessageMixin, SurveyFacilitatorMixin,
                            SurveyCreatorMixin, SurveyDetailMixin,
                            PageTitleMixin, UpdateView):
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
    success_message = _('Survey was updated successfully')

    def get_page_title(self):
        return _('Edit') + ' ' + self.object.name

    def get_success_url(self):
        return reverse('surveys:survey-edit-step-two', kwargs={'pk': self.object.pk})


class SurveyEditStepTwoView(SuccessMessageMixin, SurveyFacilitatorMixin,
                            SurveyCreatorMixin, SurveyDetailMixin,
                            PageTitleMixin, UpdateView):
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
    success_message = _('Survey was updated successfully')

    def get_page_title(self):
        return _('Edit') + ' ' + self.object.name

    def get_success_url(self):
        return reverse('surveys:survey-edit-step-three', kwargs={'pk': self.object.pk})


class SurveyEditStepThreeView(SuccessMessageMixin, SurveyFacilitatorMixin,
                              SurveyCreatorMixin, SurveyDetailMixin,
                              PageTitleMixin, UpdateView):
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
    success_message = _('Survey was updated successfully')

    def get_page_title(self):
        return _('Edit') + ' ' + self.object.name

    def get_success_url(self):
        return reverse('surveys:survey-edit-step-four', kwargs={'pk': self.object.pk})


class SurveyEditStepFourView(SuccessMessageMixin, SurveyFacilitatorMixin,
                             SurveyCreatorMixin, SurveyDetailMixin,
                             PageTitleMixin, UpdateView):
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
    success_message = _('Survey was updated successfully')

    def get_page_title(self):
        return _('Edit') + ' ' + self.object.name

    def get_success_url(self):
        return reverse('surveys:survey-edit-step-five', kwargs={'pk': self.object.pk})


class SurveyEditStepFiveView(SuccessMessageMixin, SurveyFacilitatorMixin,
                             SurveyCreatorMixin, SurveyDetailMixin,
                             PageTitleMixin, UpdateView):
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
    success_message = _('Survey was updated successfully')

    def get_page_title(self):
        return _('Edit') + ' ' + self.object.name

    def get_success_url(self):
        return reverse('surveys:survey-edit-step-six', kwargs={'pk': self.object.pk})


class SurveyEditStepSixView(SuccessMessageMixin, SurveyFacilitatorMixin,
                            SurveyCreatorMixin, SurveyDetailMixin,
                            PageTitleMixin, UpdateView):
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
    success_message = _('Survey was updated successfully')

    def get_page_title(self):
        return _('Edit') + ' ' + self.object.name

    def get_success_url(self):
        return reverse('surveys:survey-edit-finish', kwargs={'pk': self.object.pk})


class SurveyEditFinishView(SurveyFacilitatorMixin, PageTitleMixin, DetailView):
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

    def get_page_title(self):
        return _('Edit') + ' ' + self.object.name
