from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, UpdateView
from django.views.generic.list import ListView

from django_filters.views import FilterView
from invitations.utils import get_invitation_model
from invitations.views import SendInvite

from apps.responses.mixins import ConsentCheckMixin, RespondentSurveyMixin
from core.exceptions import NotAuthenticated
from core.mixins import CSVResponseMixin, PageMixin

from .filters import RespondentFilter
from .forms import RespondentConsentForm, RespondentForm, RespondentInviteForm, ResponseRespondentForm
from .mixins import RespondentFacilitatorMixin
from .models import Respondent

Invitation = get_invitation_model()

class RespondentListView(RespondentFacilitatorMixin, PageMixin, CSVResponseMixin, FilterView):
    """
    Listing respondents as a facilitator.
    """

    # Translators: This is respondents list page title
    page_title = _('Manage respondents')
    template_name = 'respondents/respondent_list.html'
    context_object_name = 'respondents'
    model = Respondent
    filterset_class = RespondentFilter
    ordering = ['-created_at']
    paginate_by = 30

    def get_queryset(self):
        return super().get_queryset()\
            .select_related('survey', 'survey__project', 'gender')\
            .with_status()

    def get_rows(self):
        yield ('id', 'email', 'first_name', 'last_name', 'gender', 'registered',
               'survey', 'survey_id', 'project', 'project_id', 'status')

        for obj in self.object_list:
            gender = obj.gender.name if obj.gender else ''
            yield (obj.id, obj.email, obj.first_name, obj.last_name, gender, obj.registered,
                   obj.survey.name, obj.survey.id, obj.survey.project.name, obj.survey.project.id, obj.status)

    def get_filename(self):
        return f'respondents-{str(timezone.now().date())}.csv'

    def get_renderer(self):
        # When `format=csv` in URL query string return csv
        if self.request.GET.get('format') == 'csv':
            return 'csv'


class RespondentConsentView(PageMixin, RespondentSurveyMixin, FormView):
    """
    Asks respondent for consent and saves consent data in user's session.

    If user is not authenicated and the survey requires login,
    user will be redirected to default ``LOGIN_URL``

    If user is a new respondent for the survey a new respondent
    object will be created.

    On successful consent user will be redirected to continue
    with the survey.
    """

    # Basing this on Survey model because at this point a user might be
    # unauthenticated or not assosiated with any respondent object.
    form_class = RespondentConsentForm
    template_name = 'respondents/respondent_consent.html'

    def dispatch(self, *args, **kwargs):
        """
        Sets survey object then continue with request processing.

        If ``NotAuthenticated`` exception was raised user will be
        redirected to ``LOGIN_URL``.
        """
        self.respondent = None

        self.survey = self.get_survey()
        try:
            self.validate_respondent_for_survey()
        except NotAuthenticated:
            return redirect_to_login(self.request.get_full_path())

        return super().dispatch(*args, **kwargs)

    def get_page_title(self):
        return self.survey.display_name

    def get_success_url(self):
        return reverse('respondents:respondent-update', kwargs={'pk': self.respondent.pk})

    def form_valid(self, form):
        """Get or create Respondent and save consent details in session."""
        # get or create respondent
        respondent_lookup = self.get_respondent_lookup()
        self.respondent = self.survey.get_or_create_respondent(**respondent_lookup)[0]

        # store consent details
        session_surveys = self.request.session.get('surveys', {})
        session_surveys[str(self.survey.pk)] = {
            'consented_at': timezone.now().isoformat()
        }
        self.request.session['surveys'] = session_surveys
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['survey'] = self.survey
        return context

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

    def get_footer_logos(self):
        return self.survey.logos.all()


class RespondentUpdateView(PageMixin, RespondentSurveyMixin, ConsentCheckMixin, UpdateView):
    """
    Prompts respondents to update their basic data for the survey.

    if consent hasn't been provided yet, user will be redirected to consent page.
    """
    model = Respondent
    form_class = ResponseRespondentForm
    context_object_name = 'respondent'
    template_name = 'respondents/respondent_update.html'

    def dispatch(self, *args, **kwargs):
        self.survey_response = None
        self.object = self.get_object()
        self.survey = self.get_survey()

        try:
            self.validate_respondent_for_survey()
        except NotAuthenticated:
            return redirect_to_login(self.request.get_full_path())

        self.consented_at = self.get_consent(respondent=self.object, survey=self.survey)
        # If respondent has not provided the consent redirect to consent page
        if not self.consented_at:
            return redirect(reverse('respondents:respondent-consent', kwargs={'survey': self.survey.pk}))

        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return self.model.objects.active().select_related('survey', 'survey__project')

    def get_object(self, queryset=None):
        # Check if self.object is already set to prevent unnecessary DB calls
        if hasattr(self, 'object'):
            return self.object
        else:
            return super().get_object(queryset)

    def get_survey(self):
        return self.object.survey

    def get_form_kwargs(self):
        """
        Add project to form class initialization arguments and return
        keyword arguments required to instantiate the form.

        https://docs.djangoproject.com/en/3.0/ref/class-based-views/mixins-editing/#django.views.generic.edit.FormMixin.get_form_kwargs
        """
        kwargs = super().get_form_kwargs()
        kwargs['survey'] = self.survey
        return kwargs

    def get_page_title(self):
        return self.survey.display_name

    def form_valid(self, form):
        """
        Update Respondent, get or create Response then redirect to response
        update page.
        """
        self.object = form.save()

        if self.request.user.is_authenticated:
            creator = self.request.user
        else:
            creator = None

        self.survey_response = self.object.get_or_create_response(
            creator=creator,
            consented_at=self.consented_at
        )[0]
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('responses:dataset-response-list-create', kwargs={'pk': self.survey_response.pk})

    def get_back_url_path(self):
        return reverse('respondents:respondent-consent', kwargs={'survey': self.survey.pk})

    def get_footer_logos(self):
        return self.survey.logos.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['hierarchy_levels'] = self.survey.project.hierarchy_levels.values('id', 'level', 'name')
        context['hierarchies'] = self.survey.project.hierarchies.values('id', 'level', 'name', 'parent')
        return context

class RespondentCreateInviteView(RespondentFacilitatorMixin, PageMixin, SendInvite):
    template_name = 'invites/create_invite.html'
    page_title = _('Create Survey Invite')
    context_object_name = 'respondents'
    queryset = Respondent.objects.all()

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        print(f'---------------{request.POST}---------------')

        if form.is_valid():
            # <process form cleaned data>
            return redirect('/respondents/invite')

        return render(request, self.template_name, {'form': form})

class RespondentSendInviteView(RespondentFacilitatorMixin, PageMixin, SendInvite):
    template_name = 'invites/create_invite.html'
    page_title = _('Create Invite')
    context_object_name = 'respondents'
    queryset = Respondent.objects.all()
    form_class= RespondentInviteForm

    # TODO: add respondent filters

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        print(f'---------------{request.POST}---------------')

        if form.is_valid():
            # <process form cleaned data>
            return redirect('/respondents/invite')

        return render(request, self.template_name, {'form': form})
