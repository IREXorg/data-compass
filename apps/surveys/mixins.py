

class SurveyCreatorMixin:
    """
    CBV mixin which puts the user from the request as survey creator in
    form instance if not exist.
    Note: Using this mixin requires `LoginRequiredMixin`.
    """
    def form_valid(self, form):
        if not form.instance.creator_id:
            form.instance.creator = self.request.user
        form.save()
        return super().form_valid(form)
