from django.db import models
from django.db.models import Case, CharField, Max, Q, Value, When


class SurveyQuerySet(models.QuerySet):

    def active(self):
        """
        Returns a queryset of active surveys.
        """
        return self.filter(is_active=True)

    def for_user(self, user=None):
        """
        Returns surveys where user is a rendondent and annotates user_status.
        """
        if not user or not user.is_authenticated:
            return self.none()

        # For each survey in the queryset;
        # If respondent is user and response has completed status then the survey is completed.
        # Otherwise if the survey is in progress.
        #
        # If respondent is not the user then the user hasn't started the survey yet.'

        queryset = self.filter(respondent__user=user)
        return queryset.annotate(
            user_status=Case(
                When(
                    Q(respondent__response__isnull=False)
                    & Q(respondent__response__completed_at__isnull=True),
                    then=Value('in progress')
                ),
                When(
                    Q(respondent__response__completed_at__isnull=False),
                    then=Value('completed')
                ),
                default=Value('not started'),
                output_field=CharField()
            ),
            respondent_id=Max('respondent__pk', filter=Q(respondent__user=user)),
            response_id=Max('respondent__response__pk', filter=Q(respondent__user=user)),
        )

    def available(self, user=None):
        """
        Returns a queryset containing Surveys that can be taken by the
        user as a respondent excluding ones where user is already a respondent.

        If user is None or AnonymousUser return all Surveys that
        don't require login.
        """
        if not user or not user.is_authenticated:
            return self.active().filter(login_required=False)

        return self.active().exclude(respondent__user=user).filter(invitation_required=False)


class SurveyManager(models.Manager):
    """Survey model manager."""

    def get_queryset(self):
        return SurveyQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def for_user(self, user=None):
        return self.get_queryset().for_user(user)

    def available(self, user=None):
        return self.get_queryset().available(user)
