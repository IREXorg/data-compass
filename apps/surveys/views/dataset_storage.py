from django.urls import reverse_lazy as reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from core.mixins import PageTitleMixin, PopupDeleteMixin, SuccessMessageMixin

from ..forms import DatasetStorageCreateForm, DatasetStorageUpdateForm
from ..mixins import (BasePopupModelFormMixin, CreatorMixin, SurveyFacilitatorRequiredMixin,
                      SurveyRelatedFacilitatorMixin)
from ..models import DatasetStorage


class DatasetStorageCreateView(SuccessMessageMixin, SurveyFacilitatorRequiredMixin,
                               CreatorMixin, PageTitleMixin,
                               BasePopupModelFormMixin, CreateView):
    """
    Create survey dataset storage view.

    Allow current signin user to create a new survey dataset storage and
    redirect to survey dataset storage edit page.

    **Example request**:

    .. code-block::

        POST  /surveys/1234567890/create-dataset-storage
    """

    # Translators: This is survey dataset storage create page title
    page_title = _('Create a survey dataset storage')
    template_name = 'surveys/survey_dataset_storage_create.html'
    context_object_name = 'dataset'
    model = DatasetStorage
    form_class = DatasetStorageCreateForm
    success_message = _('Dataset storage was created successfully')

    def get_form_kwargs(self):
        """
        Add survey to form class initialization arguments
        """
        form_kwargs = super().get_form_kwargs()
        form_kwargs['survey'] = self.survey
        return form_kwargs

    def get_success_url(self):
        return reverse('surveys:edit-step-five', kwargs={'pk': self.object.survey.pk})


class DatasetStorageUpdateView(SuccessMessageMixin, SurveyRelatedFacilitatorMixin,
                               CreatorMixin, PageTitleMixin,
                               BasePopupModelFormMixin, UpdateView):
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
    success_message = _('Dataset storage was updated successfully')

    def get_success_url(self):
        return reverse('surveys:edit-step-five', kwargs={'pk': self.object.survey.pk})


class DatasetStorageDeleteView(SuccessMessageMixin, SurveyRelatedFacilitatorMixin,
                               PageTitleMixin, PopupDeleteMixin, DeleteView):
    """
    Delete survey dataset storage view

    Allow current signin user to delete existing survey dataset storage and
    redirect to survey dataset storage edit page.

    **Example request**:

    .. code-block::

        DELETE  /surveys/1234567890/delete-dataset-storage
    """

    # Translators: This is survey dataset storage delete page title
    page_title = _('Delete a survey dataset storage')
    template_name = 'surveys/survey_dataset_storage_delete.html'
    context_object_name = 'dataset'
    model = DatasetStorage
    success_message = _('Dataset storage was deleted successfully')

    def get_success_url(self):
        return reverse('surveys:edit-step-five', kwargs={'pk': self.object.survey.pk})
