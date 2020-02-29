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


class ProjectFacilitatorMixin:
    """
    CBV mixin which limits projects queryset to only objects where the user is
    among facilitators.

    Note: Using this mixin you will need to ensure the user
    is authenticated example by using `LoginRequiredMixin`.
    """

    def get_queryset(self):
        return self.model.objects.filter(facilitators=self.request.user)
