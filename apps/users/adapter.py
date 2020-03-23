from allauth.account.adapter import DefaultAccountAdapter

from apps.respondents.models import Respondent


class AccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.

        This also connect the user with anonymous respondent objects with matching email.
        """

        user = super().save_user(request, user, form, commit=commit)

        if user.is_respondent and user.email and commit:
            Respondent.objects.filter(email=user.email, user=None).update(user=user)

        return user
