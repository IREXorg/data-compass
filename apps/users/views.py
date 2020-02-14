from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView

from core.mixins import PageTitleMixin


class ProfileView(LoginRequiredMixin, PageTitleMixin, TemplateView):
    """User's own profile view."""
    page_title = _('Profile')
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
