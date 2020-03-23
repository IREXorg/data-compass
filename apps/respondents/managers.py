from django.db import models
from django.db.models import BooleanField, Case, CharField, Q, Value, When


class RespondentQuerySet(models.QuerySet):

    def active(self):
        """
        Returns a queryset of active respondents.

        Active respondents includes respondents with active surveys.
        """
        return self.filter(survey__is_active=True)

    def with_status(self):
        """
        Return queryset with annotated status.
        """
        return self.annotate(
            status=Case(
                When(
                    Q(response__isnull=False)
                    & Q(response__completed_at__isnull=True),
                    then=Value(self.model.IN_PROGRESS)
                ),
                When(
                    Q(response__completed_at__isnull=False),
                    then=Value(self.model.COMPLETED)
                ),
                default=Value(self.model.NOT_STARTED),
                output_field=CharField()
            ),
            registered=Case(
                When(
                    Q(user__isnull=False)
                    & Q(user__is_active=True),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField()
            )
        )


class RespondentManager(models.Manager):
    """Respondent model manager."""

    def get_queryset(self):
        return RespondentQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def with_status(self):
        return self.get_queryset().with_status()
