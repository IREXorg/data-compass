from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy as reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import DeleteView, UpdateView

from core.mixins import PageTitleMixin, PopupDeleteMixin

from ..forms import TopicUpdateForm
from ..mixins import CreatorMixin, TopicPopupModelFormMixin
from ..models import Topic


class TopicUpdateView(LoginRequiredMixin, CreatorMixin, PageTitleMixin, TopicPopupModelFormMixin, UpdateView):
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
    model = Topic
    form_class = TopicUpdateForm

    def get_success_url(self):
        return reverse('surveys:edit-step-two', kwargs={'pk': self.object.survey.pk})


class TopicDeleteView(LoginRequiredMixin, PageTitleMixin, PopupDeleteMixin, DeleteView):
    """
    Delete survey topic view

    Allow current signin user to delete existing survey topic and
    redirect to survey topic edit page.

    **Example request**:

    .. code-block:: http

        DELETE  /surveys/1234567890/delete-topic
    """

    # Translators: This is survey topic delete page title
    page_title = _('Delete a survey topic')
    template_name = 'surveys/survey_topic_delete.html'
    context_object_name = 'topic'
    model = Topic

    def get_success_url(self):
        return reverse('surveys:edit-step-two', kwargs={'pk': self.object.survey.pk})
