from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from core.mixins import PopupModelFormMixin


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


class FacilitatorMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    CBV mixin which makes sure user is a facilitator.
    """

    def test_func(self):
        """
        Ensure user is a facilitator.

        Returns true if user is facilitator.
        """
        return self.request.user.is_facilitator


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
            return self.object.topics.all()

    def get_datasets(self):
        """
        Get datasets associated with the survey
        """
        if self.object:
            return self.object.datasets.all()

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
