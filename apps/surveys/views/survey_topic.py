from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy as reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import DeleteView

from core.mixins import PageTitleMixin, PopupDeleteMixin

# from ..mixins import CreatorMixin
from ..models import Topic


class SurveyTopicDeleteView(LoginRequiredMixin, PageTitleMixin, PopupDeleteMixin, DeleteView):
    """
    Delete survey topic

    Allow current signin user to delete existing survey topic and
    redirect to survey topic edit page.

    **Example request**:

    .. code-block:: http

        DELETE  /topics/1234567890/delete
    """

    # Translators: This is survey topic delete page title
    page_title = _('Delete a survey topic')
    template_name = 'surveys/survey_topic_delete.html'
    context_object_name = 'topic'
    model = Topic

    def get_success_url(self):
        return reverse('surveys:edit-step-two', kwargs={'pk': self.object.survey.pk})
