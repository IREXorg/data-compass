from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect
from django.urls import reverse_lazy as reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import CreateView

from apps.surveys.mixins import BasePopupModelFormMixin
from apps.surveys.models import Dataset, DatasetStorage, Entity, Survey
from core.exceptions import NotAuthenticated
from core.mixins import PageMixin

from ..forms import EntityCreateForm
from ..mixins import ConsentCheckMixin, RespondentSurveyMixin


class BaseCreateView(PageMixin, RespondentSurveyMixin, ConsentCheckMixin,
                     BasePopupModelFormMixin, CreateView):
    """
    Create survey role.

    Allow current respondent to create a new survey role.
    """

    page_title = _('Create a role')
    template_name = 'responses/base_response_form.html'
    fields = ['name']
    success_message = _('A role was created successfully')
    survey_lookup_url_kwarg = 'survey'
    allowed_by = None

    def get_survey_queryset(self):
        if not self.allowed_by:
            raise ValueError(_('allowed_by attribute must be defined'))
        return Survey.objects.filter(**{self.allowed_by: True}).active()

    def dispatch(self, *args, **kwargs):
        self.survey = self.get_survey()
        self.respondent = self.get_respondent()

        try:
            self.validate_respondent_for_survey()
        except NotAuthenticated:
            return redirect_to_login(self.request.get_full_path())

        self.consented_at = self.get_consent(survey=self.survey)
        # If respondent has not provided the consent redirect to consent page
        if not self.consented_at:
            return redirect(reverse('respondents:respondent-consent', kwargs={'survey': self.survey.pk}))

        return super().dispatch(*args, **kwargs)

    def get_respondent_lookup(self):
        """
        Returns parameters which can be used to check if user
        is already saved as survey respondent.
        """
        user = self.request.user
        email = self.request.GET.get('email')
        if user.is_authenticated and not email:
            email = user.email

        return {'user': user, 'email': email}

    def get_respondent(self):
        if self.survey.login_required and not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path())
        respondent_lookup = self.get_respondent_lookup()
        return self.survey.get_or_create_respondent(**respondent_lookup)[0]

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.survey = self.survey
        return super().form_valid(form)


class DatasetCreateView(BaseCreateView):
    page_title = _('Add option')
    model = Dataset
    allowed_by = 'allow_respondent_topics'


class DatasetStorageCreateView(BaseCreateView):
    page_title = _('Add storage')
    model = DatasetStorage
    allowed_by = 'allow_respondent_storages'


class EntityCreateView(BaseCreateView):
    page_title = _('Add entity')
    model = Entity
    fields = None
    form_class = EntityCreateForm
    allowed_by = 'allow_respondent_entities'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['survey'] = self.survey
        return kwargs
