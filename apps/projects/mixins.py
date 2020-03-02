from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect


class ProjectCreatorMixin:
    """
    CBV mixin which puts the user from the request as project creator in
    form instance if not exist.
    If user facilitator adds user to project facilitators list.

    Note: Using this mixin requires `LoginRequiredMixin`.
    """

    def form_valid(self, form):
        if not form.instance.creator_id:
            form.instance.creator = self.request.user
        self.object = form.save()

        if self.request.user.is_facilitator:
            self.object.facilitators.add(self.request.user)

        return redirect(self.get_success_url())


class ProjectFacilitatorMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    CBV mixin which makes sure user is a facilitator and limits project
    queryset to only objects where the user is among the facilitators.
    """

    def get_queryset(self):
        """
        Returns queryset of projects where user is among facilitators.
        """
        return self.model.objects.filter(facilitators=self.request.user)

    def test_func(self):
        """
        Ensure user is a facilitator.

        Returns true if user is facilitator.
        """
        return self.request.user.is_facilitator
