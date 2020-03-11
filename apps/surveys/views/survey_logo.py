from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy as reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from core.mixins import PageTitleMixin, PopupDeleteMixin

from ..forms import LogoCreateForm, LogoUpdateForm
from ..mixins import BasePopupModelFormMixin, CreatorMixin
from ..models import Logo, Survey


class LogoCreateView(LoginRequiredMixin, CreatorMixin, PageTitleMixin, BasePopupModelFormMixin, CreateView):
    """
    Create survey logo view.

    Allow current signin user to create a new survey and
    redirect to survey logo edit page.

    **Example request**:

    .. code-block:: http

        POST  /surveys/1234567890/create-logo
    """

    # Translators: This is survey logo create page title
    page_title = _('Create a survey logo')
    template_name = 'surveys/survey_logo_create.html'
    context_object_name = 'logo'
    model = Logo
    form_class = LogoCreateForm

    def get_survey(self):
        """
        Get survey to associate a logo with from url parameters
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
        return reverse('surveys:edit-step-six', kwargs={'pk': self.object.survey.pk})


class LogoUpdateView(LoginRequiredMixin, CreatorMixin, PageTitleMixin, BasePopupModelFormMixin, UpdateView):
    """
    Update survey logo view.

    Allow current signin user to update existing survey logo and
    redirect to survey logo edit page.

    **Example request**:

    .. code-block::

        PUT  /logos/1234567890/update-logo
    """

    # Translators: This is survey logo update page title
    page_title = _('Delete a survey logo')
    template_name = 'surveys/survey_logo_update.html'
    context_object_name = 'logo'
    model = Logo
    form_class = LogoUpdateForm

    def get_success_url(self):
        return reverse('surveys:edit-step-six', kwargs={'pk': self.object.survey.pk})


class LogoDeleteView(LoginRequiredMixin, PageTitleMixin, PopupDeleteMixin, DeleteView):
    """
    Delete survey logo view

    Allow current signin user to delete existing survey logo and
    redirect to survey logo edit page.

    **Example request**:

    .. code-block:: http

        DELETE  /surveys/1234567890/delete-logo
    """

    # Translators: This is survey logo delete page title
    page_title = _('Delete a survey logo')
    template_name = 'surveys/survey_logo_delete.html'
    context_object_name = 'logo'
    model = Logo

    def get_success_url(self):
        return reverse('surveys:edit-step-six', kwargs={'pk': self.object.survey.pk})
