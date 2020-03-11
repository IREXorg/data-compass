from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy as reverse
from django.utils.translation import ugettext_lazy as _

from invitations.utils import get_invitation_model
from invitations.views import SendInvite

from apps.projects.models import Project
from core.mixins import PageMixin
from django.views.generic.list import ListView

Invitation = get_invitation_model()

class SendInviteView(PageMixin, SendInvite, ListView):
    template_name = 'invitations/send_invite.html'
    page_title = 'Send Invite'
    context_object_name = 'respondents'
    queryset = Invitation.objects.all()

    def form_valid(self, form):
        invite = Invitation.create(form.cleaned_data['email'], inviter=self.request.user)
        invite.send_invitation(self.request)

        return redirect('/invitations/send-invite')
