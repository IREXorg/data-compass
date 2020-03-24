import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.response import TemplateResponse
from django.urls import reverse_lazy as reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from apps.users.models import Gender
from core.mixins import PageTitleMixin, PopupTemplateMixin, SuccessMessageMixin

from ..forms import GenderCreateForm, GenderUpdateForm
from ..mixins import BasePopupModelFormMixin, SurveyFacilitatorRequiredMixin


class GenderCreateView(SuccessMessageMixin, SurveyFacilitatorRequiredMixin,
                       PageTitleMixin, BasePopupModelFormMixin, CreateView):
    """
    Create survey gender view.

    Allow current signin user to create a new survey gender and
    redirect to survey gender edit page.

    **Example request**:

    .. code-block::

        POST  /surveys/1234567890/create-gender
    """

    # Translators: This is survey gender create page title
    page_title = _('Create a survey gender')
    template_name = 'surveys/survey_gender_create.html'
    context_object_name = 'gender'
    model = Gender
    form_class = GenderCreateForm
    success_message = _('Gender was created successfully')

    def get_form_kwargs(self):
        """
        Add survey to form class initialization arguments
        """
        form_kwargs = super().get_form_kwargs()
        form_kwargs['survey'] = self.survey
        return form_kwargs

    def get_success_url(self):
        return reverse('surveys:edit-step-six', kwargs={'pk': self.object.survey.pk})


class GenderUpdateView(SuccessMessageMixin, LoginRequiredMixin,
                       PageTitleMixin, BasePopupModelFormMixin, UpdateView):
    """
    Update survey gender view.

    Allow current signin user to update existing survey gender and
    redirect to survey gender edit page.

    **Example request**:

    .. code-block::

        PUT  /genders/1234567890/update-gender
    """

    # Translators: This is survey gender update page title
    page_title = _('Delete a survey gender')
    template_name = 'surveys/survey_gender_update.html'
    context_object_name = 'gender'
    model = Gender
    form_class = GenderUpdateForm
    success_message = _('Gender was updated successfully')

    def get_queryset(self):
        return Gender.objects.filter(
            is_primary=False,
            survey__project__facilitators=self.request.user
        )

    def get_success_url(self):
        return reverse('surveys:edit-step-six', kwargs={'pk': self.object.survey.pk})


class GenderDeleteView(SuccessMessageMixin, SurveyFacilitatorRequiredMixin, PageTitleMixin,
                       PopupTemplateMixin, DeleteView):
    """
    Delete survey gender view

    Allow current signin user to delete existing survey gender and
    redirect to survey gender edit page.

    **Example request**:

    .. code-block::

        DELETE  /surveys/1234567890/delete-gender
    """

    # Translators: This is survey gender delete page title
    page_title = _('Delete a survey gender')
    template_name = 'surveys/survey_gender_delete.html'
    context_object_name = 'gender'
    model = Gender
    success_message = _('Gender was deleted successfully')

    def get_queryset(self):
        return Gender.objects.filter(
            is_primary=False,
            survey__project__facilitators=self.request.user
        )

    def get_success_url(self):
        return reverse('surveys:edit-step-six', kwargs={'pk': self.object.survey.pk})

    def delete(self, request, *args, **kwargs):

        if self.is_popup():
            self.object = self.get_object()

            if self.object.is_primary:
                # di-associate primary/shared gender
                # and don't delete
                self.survey.genders.remove(self.object)
            else:
                # delete non-primary/non-shared gender
                self.object.delete()

            popup_response_data = json.dumps({
                'action': 'delete_object',
            })

            return TemplateResponse(
                self.request,
                'core/popup_response.html',
                {'popup_response_data': popup_response_data}
            )

        return super().delete(request, *args, **kwargs)
