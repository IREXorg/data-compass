from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, TemplateView

from core.mixins import PageTitleMixin

from .forms import ProfileForm


class ProfileView(LoginRequiredMixin, PageTitleMixin, TemplateView):
    """User's own profile view."""
    page_title = _('Profile')
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class ProfileUpdateView(LoginRequiredMixin, PageTitleMixin, FormView):
    """User own profile update view."""
    model = get_user_model()
    form_class = ProfileForm
    page_title = _('Update Profile')
    template_name = 'users/profile_update.html'

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs.update({'instance': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse('users:profile-detail')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)