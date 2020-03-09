from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy as reverse
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect

from apps.projects.models import Project
from core.mixins import PageTitleMixin

from invitations.utils import get_invitation_model
from invitations.views import SendInvite

Invitation = get_invitation_model()

class SendInviteView(SendInvite):
    template_name='invitations/send_invite.html'
    page_title='Send Invite'

    def form_valid(self, form):
        print(f'-----{self.request}-----')
        print(f'-----{form.cleaned_data}-----')

        invite = Invitation.create(form.cleaned_data['email'], inviter=self.request.user)
        invite.send_invitation(self.request)

        return redirect('/invitations/send-invite')


