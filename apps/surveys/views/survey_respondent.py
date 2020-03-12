from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy as reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from core.mixins import PageTitleMixin, PopupDeleteMixin

from ..forms import RespondentCreateForm, RespondentUpdateForm
from ..mixins import BasePopupModelFormMixin, CreatorMixin
from ..models import Respondent, Survey


class RespondentCreateView(LoginRequiredMixin, CreatorMixin, PageTitleMixin, BasePopupModelFormMixin, CreateView):
    """
    Create survey respondent view.

    Allow current signin user to create a new survey and
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


class RespondentUpdateView(LoginRequiredMixin, CreatorMixin, PageTitleMixin, BasePopupModelFormMixin, UpdateView):
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

    def get_success_url(self):
        return reverse('surveys:edit-step-one', kwargs={'pk': self.object.survey.pk})


class RespondentDeleteView(LoginRequiredMixin, PageTitleMixin, PopupDeleteMixin, DeleteView):
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

    def get_success_url(self):
        return reverse('surveys:edit-step-one', kwargs={'pk': self.object.survey.pk})
