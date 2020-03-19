from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy as reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from apps.respondents.models import Respondent
from core.mixins import PageTitleMixin, PopupDeleteMixin, SuccessMessageMixin

from ..forms import RespondentCreateForm, RespondentsUploadForm, RespondentUpdateForm
from ..mixins import BasePopupModelFormMixin, CreatorMixin
from ..models import Survey


class RespondentCreateView(SuccessMessageMixin, LoginRequiredMixin, CreatorMixin,
                           PageTitleMixin, BasePopupModelFormMixin, CreateView):
    """
    Create survey respondent view.

    Allow current signin user to create a new survey respondent and
    redirect to survey respondent edit page.

    **Example request**:

    .. code-block:: http

        POST  /surveys/1234567890/create-respondent
    """

    # Translators: This is survey respondent create page title
    page_title = _('Create a survey respondent')
    template_name = 'surveys/survey_respondent_create.html'
    context_object_name = 'respondent'
    model = Respondent
    form_class = RespondentCreateForm
    success_message = _('Respondent was created successfully')

    def get_survey(self):
        """
        Get survey to associate a respondent with from url parameters
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
        return reverse('surveys:edit-step-one', kwargs={'pk': self.object.survey.pk})


class RespondentUpdateView(SuccessMessageMixin, LoginRequiredMixin, CreatorMixin,
                           PageTitleMixin, BasePopupModelFormMixin, UpdateView):
    """
    Update survey respondent view.

    Allow current signin user to update existing survey respondent and
    redirect to survey respondent edit page.

    **Example request**:

    .. code-block::

        PUT  /respondents/1234567890/update-respondent
    """

    # Translators: This is survey respondent update page title
    page_title = _('Delete a survey respondent')
    template_name = 'surveys/survey_respondent_update.html'
    context_object_name = 'respondent'
    model = Respondent
    form_class = RespondentUpdateForm
    success_message = _('Respondent was updated successfully')

    def get_success_url(self):
        return reverse('surveys:edit-step-one', kwargs={'pk': self.object.survey.pk})


class RespondentDeleteView(SuccessMessageMixin, LoginRequiredMixin, PageTitleMixin,
                           PopupDeleteMixin, DeleteView):
    """
    Delete survey respondent view

    Allow current signin user to delete existing survey respondent and
    redirect to survey respondent edit page.

    **Example request**:

    .. code-block:: http

        DELETE  /surveys/1234567890/delete-respondent
    """

    # Translators: This is survey respondent delete page title
    page_title = _('Delete a survey respondent')
    template_name = 'surveys/survey_respondent_delete.html'
    context_object_name = 'respondent'
    model = Respondent
    success_message = _('Respondent was deleted successfully')

    def get_success_url(self):
        return reverse('surveys:edit-step-one', kwargs={'pk': self.object.survey.pk})


class RespondentsUploadView(SuccessMessageMixin, LoginRequiredMixin,
                            PageTitleMixin, BasePopupModelFormMixin, UpdateView):
    """
    Upload survey respondents view.

    Allow current signin user to upload survey respondents and
    redirect to survey respondents edit page.

    **Example request**:

    .. code-block:: http

        POST  /surveys/1234567890/upload-respondents
    """

    # Translators: This is survey respondents upload page title
    page_title = _('Upload survey respondents')
    template_name = 'surveys/survey_respondent_upload.html'
    context_object_name = 'survey'
    model = Survey
    form_class = RespondentsUploadForm
    success_message = _('Respondents was uploaded successfully')

    def get_form_kwargs(self):
        """
        Add current use to form class initialization arguments
        """
        form_kwargs = super().get_form_kwargs()
        if self.request.user:
            form_kwargs['creator'] = self.request.user
        return form_kwargs

    # TODO: ensure creator

    def get_success_url(self):
        return reverse('surveys:edit-step-one', kwargs={'pk': self.object.pk})
