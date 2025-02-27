from django.urls import reverse_lazy as reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from core.mixins import PageTitleMixin, PopupDeleteMixin, SuccessMessageMixin

from ..forms import QuestionCreateForm, QuestionUpdateForm
from ..mixins import (BasePopupModelFormMixin, CreatorMixin, SurveyFacilitatorRequiredMixin,
                      SurveyRelatedFacilitatorMixin)
from ..models import Question


class QuestionCreateView(SuccessMessageMixin, SurveyFacilitatorRequiredMixin, CreatorMixin,
                         PageTitleMixin, BasePopupModelFormMixin, CreateView):
    """
    Create survey question view.

    Allow current signin user to create a new survey question and
    redirect to survey question edit page.

    **Example request**:

    .. code-block:: http

        POST  /surveys/1234567890/create-question
    """

    # Translators: This is survey question create page title
    page_title = _('Create a survey question')
    template_name = 'surveys/survey_question_create.html'
    context_object_name = 'question'
    model = Question
    form_class = QuestionCreateForm
    success_message = _('Question was created successfully')

    def get_form_kwargs(self):
        """
        Add survey to form class initialization arguments
        """
        form_kwargs = super().get_form_kwargs()
        form_kwargs['survey'] = self.survey
        return form_kwargs

    def get_success_url(self):
        return reverse('surveys:edit-step-six', kwargs={'pk': self.object.survey.pk})


class QuestionUpdateView(SuccessMessageMixin, SurveyRelatedFacilitatorMixin, CreatorMixin,
                         PageTitleMixin, BasePopupModelFormMixin, UpdateView):
    """
    Update survey question view.

    Allow current signin user to update existing survey question and
    redirect to survey question edit page.

    **Example request**:

    .. code-block::

        PUT  /questions/1234567890/update-question
    """

    # Translators: This is survey question update page title
    page_title = _('Delete a survey question')
    template_name = 'surveys/survey_question_update.html'
    context_object_name = 'question'
    model = Question
    form_class = QuestionUpdateForm
    success_message = _('Question was updated successfully')

    def get_success_url(self):
        return reverse('surveys:edit-step-six', kwargs={'pk': self.object.survey.pk})


class QuestionDeleteView(SuccessMessageMixin, SurveyRelatedFacilitatorMixin, PageTitleMixin,
                         PopupDeleteMixin, DeleteView):
    """
    Delete survey question view

    Allow current signin user to delete existing survey question and
    redirect to survey question edit page.

    **Example request**:

    .. code-block:: http

        DELETE  /surveys/1234567890/delete-question
    """

    # Translators: This is survey question delete page title
    page_title = _('Delete a survey question')
    template_name = 'surveys/survey_question_delete.html'
    context_object_name = 'question'
    model = Question
    success_message = _('Question was deleted successfully')

    def get_success_url(self):
        return reverse('surveys:edit-step-six', kwargs={'pk': self.object.survey.pk})
