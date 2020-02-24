from django.db import models
from django.db.models import Case, CharField, Q, Value, When


class SurveyQuerySet(models.QuerySet):

    def active(self):
        """
        Returns a queryset of active surveys.
        """
        return self.filter(is_active=True)

    def for_user(self, user=None):
        """
        Returns a queryset containing Surveys that can be taken by the
        user as a respondent.

        If user is None or AnonymousUser return all Surveys that
        don't require login.

        If the user object is not anonymous user_status will be
        annotated to the queryset.
        """
        if not user or not user.is_authenticated:
            return self.filter(login_required=False)

        qs = self.filter(Q(invitation_required=False) | Q(respondent__user=user))

        # For each survey in the queryset;
        # If respondent is user and response has completed status then the survey is completed.
        # Otherwise if the survey is in progress.
        #
        # If respondent is not the user then the user hasn't started the survey yet.'
        return qs.annotate(
            user_status=Case(
                When(
                    Q(respondent__user=user) & Q(respondent__response__completed_at__isnull=True),
                    then=Value('in progress')
                ),
                When(
                    Q(respondent__user=user) & Q(respondent__response__completed_at__isnull=False),
                    then=Value('completed')
                ),
                default=Value('not started'),
                output_field=CharField()
            )
        )


class SurveyManager(models.Manager):
    """Survey model manager."""

    def get_queryset(self):
        return SurveyQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def for_user(self, user=None):
        return self.get_queryset().for_user(user)