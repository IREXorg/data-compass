from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy as reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from core.mixins import PageTitleMixin, PopupDeleteMixin

from ..forms import DatasetStorageCreateForm, DatasetStorageUpdateForm
from ..mixins import BasePopupModelFormMixin
from ..models import DatasetStorage, Survey

# TODO: CreatorMixin


class DatasetStorageCreateView(LoginRequiredMixin, PageTitleMixin, BasePopupModelFormMixin, CreateView):
    """
    Create survey dataset storage view.

    Allow current signin user to create a new survey and
    redirect to survey dataset storage edit page.

    **Example request**:

    .. code-block:: http

        POST  /surveys/1234567890/create-dataset-storage
    """

    # Translators: This is survey dataset storage create page title
    page_title = _('Create a survey dataset storage')
    template_name = 'surveys/survey_dataset_storage_create.html'
    context_object_name = 'dataset'
    model = DatasetStorage
    form_class = DatasetStorageCreateForm

    def get_survey(self):
        """
        Get survey to associate a dataset storage with from url parameters
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
        return reverse('surveys:edit-step-five', kwargs={'pk': self.object.survey.pk})


class DatasetStorageUpdateView(LoginRequiredMixin, PageTitleMixin, BasePopupModelFormMixin, UpdateView):
    """
    Update survey dataset storage view.

    Allow current signin user to update existing survey dataset storage and
    redirect to survey dataset storage edit page.

    **Example request**:

    .. code-block::

        PUT  /datasets/1234567890/update-dataset-storage
    """

    # Translators: This is survey dataset storage update page title
    page_title = _('Delete a survey dataset storage')
    template_name = 'surveys/survey_dataset_storage_update.html'
    context_object_name = 'dataset'
    model = DatasetStorage
    form_class = DatasetStorageUpdateForm

    def get_success_url(self):
        return reverse('surveys:edit-step-five', kwargs={'pk': self.object.survey.pk})


class DatasetStorageDeleteView(LoginRequiredMixin, PageTitleMixin, PopupDeleteMixin, DeleteView):
    """
    Delete survey dataset storage view

    Allow current signin user to delete existing survey dataset storage and
    redirect to survey dataset storage edit page.

    **Example request**:

    .. code-block:: http

        DELETE  /surveys/1234567890/delete-dataset-storage
    """

    # Translators: This is survey dataset storage delete page title
    page_title = _('Delete a survey dataset storage')
    template_name = 'surveys/survey_dataset_storage_delete.html'
    context_object_name = 'dataset'
    model = DatasetStorage

    def get_success_url(self):
        return reverse('surveys:edit-step-five', kwargs={'pk': self.object.survey.pk})
