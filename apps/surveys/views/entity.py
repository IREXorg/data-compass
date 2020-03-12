from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy as reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from core.mixins import PageTitleMixin, PopupDeleteMixin

from ..forms import EntityCreateForm, EntityUpdateForm
from ..mixins import BasePopupModelFormMixin, CreatorMixin
from ..models import Entity, Survey


class EntityCreateView(LoginRequiredMixin, CreatorMixin, PageTitleMixin, BasePopupModelFormMixin, CreateView):
    """
    Create survey entity view.

    Allow current signin user to create a new survey and
    redirect to survey entity edit page.

    **Example request**:

    .. code-block::

        POST  /surveys/1234567890/create-entity
    """

    # Translators: This is survey entity create page title
    page_title = _('Create a survey entity')
    template_name = 'surveys/survey_entity_create.html'
    context_object_name = 'entity'
    model = Entity
    form_class = EntityCreateForm

    def get_survey(self):
        """
        Get survey to associate a entity with from url parameters
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
        return reverse('surveys:edit-step-four', kwargs={'pk': self.object.survey.pk})


class EntityUpdateView(LoginRequiredMixin, CreatorMixin, PageTitleMixin, BasePopupModelFormMixin, UpdateView):
    """
    Update survey entity view.

    Allow current signin user to update existing survey entity and
    redirect to survey entity edit page.

    **Example request**:

    .. code-block::

        PUT  /entitys/1234567890/update-entity
    """

    # Translators: This is survey entity update page title
    page_title = _('Delete a survey entity')
    template_name = 'surveys/survey_entity_update.html'
    context_object_name = 'entity'
    model = Entity
    form_class = EntityUpdateForm

    def get_success_url(self):
        return reverse('surveys:edit-step-four', kwargs={'pk': self.object.survey.pk})


class EntityDeleteView(LoginRequiredMixin, PageTitleMixin, PopupDeleteMixin, DeleteView):
    """
    Delete survey entity view

    Allow current signin user to delete existing survey entity and
    redirect to survey entity edit page.

    **Example request**:

    .. code-block::

        DELETE  /surveys/1234567890/delete-entity
    """

    # Translators: This is survey entity delete page title
    page_title = _('Delete a survey entity')
    template_name = 'surveys/survey_entity_delete.html'
    context_object_name = 'entity'
    model = Entity

    def get_success_url(self):
        return reverse('surveys:edit-step-four', kwargs={'pk': self.object.survey.pk})
