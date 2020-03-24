from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404

from apps.projects.models import Project
from core.mixins import FacilitatorMixin, PopupModelFormMixin

from .models import Survey


class CreatorMixin:
    """
    CBV mixin which puts the user from the request as creator in
    form instance if not exist.

    Note: Using this mixin requires `LoginRequiredMixin`.
    """
    def form_valid(self, form):
        if not form.instance.creator_id:
            form.instance.creator = self.request.user
        return super().form_valid(form)


class SurveyCreatorMixin:
    """
    CBV mixin which puts the user from the request as survey creator in
    form instance if not exist.

    Note: Using this mixin requires `LoginRequiredMixin`.
    """
    def form_valid(self, form):
        if not form.instance.creator_id:
            form.instance.creator = self.request.user
        return super().form_valid(form)


class SurveyFacilitatorMixin(FacilitatorMixin):
    """
    CBV mixin which makes sure user is a facilitator and limits survey
    queryset to only objects where the user is among the project facilitators.
    """

    def get_queryset(self):
        """
        Returns queryset of surveys where user is project facilitators.
        """
        return self.model.objects.filter(project__facilitators=self.request.user)


class ProjectFacilitatorRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not self.request.user.is_facilitator:
            raise PermissionDenied()

        self.project = self.get_project()

        return super().dispatch(request, *args, **kwargs)

    def get_project_queryset(self):
        return Project.objects.filter(facilitators=self.request.user)

    def get_project(self):
        project_pk = self.kwargs.get('project', None)
        if not project_pk:
            raise AttributeError(
                "%s must be called with project in the URLconf."
                % self.__class__.__name__
            )

        try:
            return self.get_project_queryset().get(pk=project_pk)
        except Project.DoesNotExist:
            raise Http404()


class SurveyRelatedFacilitatorMixin(FacilitatorMixin):
    """
    CBV mixin which makes sure user is a facilitator and limits survey
    queryset to only objects where the user is among the project facilitators.
    """

    def get_queryset(self):
        """
        Returns queryset of surveys where user is project facilitators.
        """
        return self.model.objects.filter(survey__project__facilitators=self.request.user)


class SurveyFacilitatorRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not self.request.user.is_facilitator:
            raise PermissionDenied()

        self.survey = self.get_survey()

        return super().dispatch(request, *args, **kwargs)

    def get_survey(self):
        survey_pk = self.kwargs.get('survey_pk', None)
        if not survey_pk:
            raise AttributeError(
                "%s must be called with survey in the URLconf."
                % self.__class__.__name__
            )
        try:
            return Survey.objects.filter(project__facilitators=self.request.user).get(pk=survey_pk)
        except Survey.DoesNotExist:
            raise Http404()


class SurveyDetailMixin:
    """
    CBV mixin which puts releated survey objects into context data.

    Note: Using this mixin requires `LoginRequiredMixin`.
    """
    def get_topics(self):
        """
        Get topics associated with the survey
        """
        if self.object:
            # TODO: restore to self.object.topics.all()
            return self.object.datasets.all()

    def get_datasets(self):
        """
        Get datasets associated with the survey
        """
        if self.object:
            # TODO: restore to self.object.datasets.all()
            return self.object.topics.all()

    def get_dataset_storages(self):
        """
        Get dataset storages associated with the survey
        """
        if self.object:
            return self.object.dataset_storages.all()

    def get_entities(self):
        """
        Get entities associated with the survey
        """
        if self.object:
            return self.object.entities.all()

    def get_roles(self):
        """
        Get roles associated with the survey
        """
        if self.object:
            return self.object.roles.all()

    def get_logos(self):
        """
        Get logos associated with the survey
        """
        if self.object:
            return self.object.logos.all()

    def get_respondents(self):
        """
        Get respondents associated with the survey but limit to 5
        """
        if self.object:
            return self.object.respondents.all()[:5]

    def get_questions(self):
        """
        Get questions associated with the survey
        """
        if self.object:
            return self.object.questions.all()

    def get_genders(self):
        """
        Get genders associated with the survey
        """
        if self.object:
            return self.object.genders.all()

    def get_context_data(self, **kwargs):
        """
        Add survey releated objects context data
        """
        context = super().get_context_data(**kwargs)
        topics = self.get_topics()
        datasets = self.get_datasets()
        dataset_storages = self.get_dataset_storages()
        entities = self.get_entities()
        roles = self.get_roles()
        logos = self.get_logos()
        respondents = self.get_respondents()
        questions = self.get_questions()
        genders = self.get_genders()
        if topics:
            context['topics'] = topics
        if datasets:
            context['datasets'] = datasets
        if dataset_storages:
            context['dataset_storages'] = dataset_storages
        if entities:
            context['entities'] = entities
        if roles:
            context['roles'] = roles
        if logos:
            context['logos'] = logos
        if respondents:
            context['respondents'] = respondents
        if questions:
            context['questions'] = questions
        if genders:
            context['genders'] = genders
        return context


class BasePopupModelFormMixin(PopupModelFormMixin):
    """
    CBV mixin to allow popup model form on edits.
    """
    def get_popup_response_data(self):
        return {
            'action': 'change_object',
            'value': str(self.object.pk),
            'obj': str(self.object),
            'new_value': str(self.object.pk),
        }
