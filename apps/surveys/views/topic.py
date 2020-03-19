from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy as reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from core.mixins import PageTitleMixin, PopupDeleteMixin, SuccessMessageMixin

from ..forms import TopicCreateForm, TopicUpdateForm
from ..mixins import BasePopupModelFormMixin, CreatorMixin
from ..models import Dataset, Survey


class TopicCreateView(SuccessMessageMixin, LoginRequiredMixin, CreatorMixin,
                      PageTitleMixin, BasePopupModelFormMixin, CreateView):
    """
    Create survey topic view.

    Allow current signin user to create a new survey topic and
    redirect to survey topic edit page.

    **Example request**:

    .. code-block::

        POST  /surveys/1234567890/create-topic
    """

    # Translators: This is survey topic create page title
    page_title = _('Create a survey topic')
    template_name = 'surveys/survey_topic_create.html'
    context_object_name = 'topic'
    model = Dataset  # TODO: restore to Topic
    form_class = TopicCreateForm
    success_message = _('Topic was created successfully')

    def get_survey(self):
        """
        Get survey to associate a topic with from url parameters
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
        return reverse('surveys:edit-step-two', kwargs={'pk': self.object.survey.pk})


class TopicUpdateView(SuccessMessageMixin, LoginRequiredMixin, CreatorMixin,
                      PageTitleMixin, BasePopupModelFormMixin, UpdateView):
    """
    Update survey topic view.

    Allow current signin user to update existing survey topic and
    redirect to survey topic edit page.

    **Example request**:

    .. code-block::

        PUT  /topics/1234567890/update-topic
    """

    # Translators: This is survey topic update page title
    page_title = _('Delete a survey topic')
    template_name = 'surveys/survey_topic_update.html'
    context_object_name = 'topic'
    model = Dataset  # TODO: restore to Topic
    form_class = TopicUpdateForm
    success_message = _('Topic was updated successfully')

    def get_success_url(self):
        return reverse('surveys:edit-step-two', kwargs={'pk': self.object.survey.pk})


class TopicDeleteView(SuccessMessageMixin, LoginRequiredMixin, PageTitleMixin,
                      PopupDeleteMixin, DeleteView):
    """
    Delete survey topic view

    Allow current signin user to delete existing survey topic and
    redirect to survey topic edit page.

    **Example request**:

    .. code-block::

        DELETE  /surveys/1234567890/delete-topic
    """

    # Translators: This is survey topic delete page title
    page_title = _('Delete a survey topic')
    template_name = 'surveys/survey_topic_delete.html'
    context_object_name = 'topic'
    model = Dataset  # TODO: restore to Topic
    success_message = _('Topic was deleted successfully')

    def get_success_url(self):
        return reverse('surveys:edit-step-two', kwargs={'pk': self.object.survey.pk})
