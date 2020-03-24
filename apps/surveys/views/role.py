from django.urls import reverse_lazy as reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from core.mixins import PageTitleMixin, PopupDeleteMixin, SuccessMessageMixin

from ..forms import RoleCreateForm, RoleUpdateForm
from ..mixins import (BasePopupModelFormMixin, CreatorMixin, SurveyFacilitatorRequiredMixin,
                      SurveyRelatedFacilitatorMixin)
from ..models import Role


class RoleCreateView(SuccessMessageMixin, SurveyFacilitatorRequiredMixin, CreatorMixin,
                     PageTitleMixin, BasePopupModelFormMixin, CreateView):
    """
    Create survey role view.

    Allow current signin user to create a new survey role and
    redirect to survey role edit page.

    **Example request**:

    .. code-block::

        POST  /surveys/1234567890/create-role
    """

    # Translators: This is survey role create page title
    page_title = _('Create a survey role')
    template_name = 'surveys/survey_role_create.html'
    context_object_name = 'role'
    model = Role
    form_class = RoleCreateForm
    success_message = _('Role was created successfully')

    def get_form_kwargs(self):
        """
        Add survey to form class initialization arguments
        """
        form_kwargs = super().get_form_kwargs()
        form_kwargs['survey'] = self.survey
        return form_kwargs

    def get_success_url(self):
        return reverse('surveys:edit-step-one', kwargs={'pk': self.object.survey.pk})


class RoleUpdateView(SuccessMessageMixin, SurveyRelatedFacilitatorMixin, CreatorMixin,
                     PageTitleMixin, BasePopupModelFormMixin, UpdateView):
    """
    Update survey role view.

    Allow current signin user to update existing survey role and
    redirect to survey role edit page.

    **Example request**:

    .. code-block::

        PUT  /roles/1234567890/update-role
    """

    # Translators: This is survey role update page title
    page_title = _('Delete a survey role')
    template_name = 'surveys/survey_role_update.html'
    context_object_name = 'role'
    model = Role
    form_class = RoleUpdateForm
    success_message = _('Role was updated successfully')

    def get_success_url(self):
        return reverse('surveys:edit-step-one', kwargs={'pk': self.object.survey.pk})


class RoleDeleteView(SuccessMessageMixin, SurveyRelatedFacilitatorMixin, PageTitleMixin,
                     PopupDeleteMixin, DeleteView):
    """
    Delete survey role view

    Allow current signin user to delete existing survey role and
    redirect to survey role edit page.

    **Example request**:

    .. code-block::

        DELETE  /surveys/1234567890/delete-role
    """

    # Translators: This is survey role delete page title
    page_title = _('Delete a survey role')
    template_name = 'surveys/survey_role_delete.html'
    context_object_name = 'role'
    model = Role
    success_message = _('Role was deleted successfully')

    def get_success_url(self):
        return reverse('surveys:edit-step-one', kwargs={'pk': self.object.survey.pk})
