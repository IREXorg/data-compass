from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, UpdateView

from core.exceptions import NotAuthenticated
from core.mixins import PageTitleMixin

from ..forms import RespondentConsentForm, RespondentForm
from ..models import Respondent, Survey


class RespondentSurveyMixin:
    """
    Provides ability to retrive a Survey object for user as a respondent.
    """

    slug_field = 'pk'
    slug_url_kwarg = 'pk'

    def get_queryset(self):
        """Get queryset of all active surveys."""
        return Survey.objects.filter(is_active=True)

    def get_survey(self):
        """
        Return survey object from queryset.

        If the user is not authenicated and survey requires login,
        raise ``NotAuthenticated``.

        If invitation is required and user is not on respondent
        list or not authenticated raise ``PermissionDenied``
        """

        # get lookup parameters
        slug = self.kwargs.get(self.slug_url_kwarg)
        if not slug:
            raise AttributeError(
                _(f'{self.__class__.__name__} view must be called with {self.slug_url_kwarg}.')
            )

        # get survey object matching the query
        try:
            survey = self.get_queryset().get(**{self.slug_field: slug})
        except Survey.DoesNotExist:
            raise Http404(_('Page not found.'))

        # ensure user is allowed to take the survey
        if not self.request.user.is_authenticated and survey.login_required:
            raise NotAuthenticated

        if survey.invitation_required and (
                not self.request.user.is_authenticated
                or not survey.respondents.filter(user=self.request.user).exists()):
            raise PermissionDenied(_('You are not allowed to take this survey'))

        return survey


class RespondentConsentView(PageTitleMixin, RespondentSurveyMixin, FormView):
    """Ask respondent for consent.

    If the user is not authenicated and survey requires login,
    redirect user to ``LOGIN_URL``
    """

    # Basing this on Survey model because at this point a user might be
    # unauthenticated or not assosiated with any respondent object.
    context_object_name = 'survey'
    template_name = 'surveys/respondent_consent.html'
    form_class = RespondentConsentForm

    def dispatch(self, *args, **kwargs):
        """
        Sets survey object then continue with request processing.

        If ``NotAuthenticated`` exception was raised user will be
        redirected to ``LOGIN_URL``.
        """
        try:
            self.survey = self.get_survey()
        except NotAuthenticated:
            return redirect_to_login(self.request.get_full_path())
        self.respondent = None
        return super().dispatch(*args, **kwargs)

    def get_page_title(self):
        return f'{self.survey.display_name}'

    def get_success_url(self):
        return reverse('surveys:respondent-update', kwargs={'pk': self.respondent.pk})

    def form_valid(self, form):
        """Get or create Respondent and save consent details in session."""
        # get or create respondent
        respondent_lookup = self.get_respondent_lookup()
        self.respondent = self.survey.get_or_create_respondent(**respondent_lookup)[0]

        # store consent details
        session_surveys = self.request.session.get('surveys', {})
        session_surveys[self.survey.pk] = {
            'consented_at': timezone.now().isoformat()
        }
        self.request.session['surveys'] = session_surveys
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_object_name] = self.survey
        return context

    def get_respondent_lookup(self):
        """
        Returns parameters which can be used to check if user
        is already saved as survey respondent.
        """
        user = self.request.user
        email = self.request.GET.get('email')
        if user and not email:
            email = user.email

        return {'user': user, 'email': email}


class RespondentUpdateView(UpdateView):
    """A naive Respondent Update View"""
    model = Respondent
    form_class = RespondentForm
    template_name = 'surveys/respondent_update.html'

    def get_queryset(self):
        return self.model.objects.select_related('survey', 'survey__project')

    def get_form_kwargs(self):
        """
        Add project to form class initialization arguments and return
        keyword arguments required to instantiate the form.

        https://docs.djangoproject.com/en/3.0/ref/class-based-views/mixins-editing/#django.views.generic.edit.FormMixin.get_form_kwargs
        """
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.object.survey.project
        return kwargs

    def get_success_url(self):
        return reverse('users:profile-detail')
