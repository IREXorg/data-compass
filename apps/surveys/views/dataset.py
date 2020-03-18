from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy as reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from core.mixins import PageTitleMixin, PopupDeleteMixin, SuccessMessageMixin

from ..forms import DatasetCreateForm, DatasetUpdateForm
from ..mixins import BasePopupModelFormMixin, CreatorMixin
from ..models import Dataset, Survey


class DatasetCreateView(SuccessMessageMixin, LoginRequiredMixin, CreatorMixin,
                        PageTitleMixin, BasePopupModelFormMixin, CreateView):
    """
    Create survey dataset view.

    Allow current signin user to create a new survey and
    redirect to survey dataset edit page.

    **Example request**:

    .. code-block::

        POST  /surveys/1234567890/create-dataset
    """

    # Translators: This is survey dataset create page title
    page_title = _('Create a survey dataset')
    template_name = 'surveys/survey_dataset_create.html'
    context_object_name = 'dataset'
    model = Dataset
    form_class = DatasetCreateForm
    success_message = _('Dataset was created successfully')

    def get_survey(self):
        """
        Get survey to associate a dataset with from url parameters
        """
        survey_pk = self.kwargs.get('survey_pk', None)
        if survey_pk:
            return Survey.objects.get(pk=survey_pk)

    def get_form_kwargs(self):
        """
        Add survey to form class initialization arguments
        """
        form_kwargs = super().get_form_kwargs()
        survey = self.get_survey()
        if survey:
            form_kwargs['survey'] = survey
        return form_kwargs

    def get_success_url(self):
        return reverse('surveys:edit-step-three', kwargs={'pk': self.object.survey.pk})


class DatasetUpdateView(SuccessMessageMixin, LoginRequiredMixin, CreatorMixin,
                        PageTitleMixin, BasePopupModelFormMixin, UpdateView):
    """
    Update survey dataset view.

    Allow current signin user to update existing survey dataset and
    redirect to survey dataset edit page.

    **Example request**:

    .. code-block::

        PUT  /datasets/1234567890/update-dataset
    """

    # Translators: This is survey dataset update page title
    page_title = _('Delete a survey dataset')
    template_name = 'surveys/survey_dataset_update.html'
    context_object_name = 'dataset'
    model = Dataset
    form_class = DatasetUpdateForm
    success_message = _('Dataset was updated successfully')

    def get_success_url(self):
        return reverse('surveys:edit-step-three', kwargs={'pk': self.object.survey.pk})


class DatasetDeleteView(SuccessMessageMixin, LoginRequiredMixin, PageTitleMixin, PopupDeleteMixin, DeleteView):
    """
    Delete survey dataset view

    Allow current signin user to delete existing survey dataset and
    redirect to survey dataset edit page.

    **Example request**:

    .. code-block::

        DELETE  /surveys/1234567890/delete-dataset
    """

    # Translators: This is survey dataset delete page title
    page_title = _('Delete a survey dataset')
    template_name = 'surveys/survey_dataset_delete.html'
    context_object_name = 'dataset'
    model = Dataset
    success_message = _('Survey was deleted successfully')

    def get_success_url(self):
        return reverse('surveys:edit-step-three', kwargs={'pk': self.object.survey.pk})
