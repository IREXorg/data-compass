from django.db import models
from django.db.models import Case, CharField, Q, Value, When


class SurveyResponseQuerySet(models.QuerySet):

    def active(self):
        """Returns a queryset of active survey responses."""
        return self.filter(survey__is_active=True)

    def with_status(self):
        """
        Return queryset with annotated status.
        """
        return self.annotate(
            status=Case(
                When(
                    Q(completed_at__isnull=False),
                    then=Value(self.model.COMPLETED)
                ),
                When(
                    Q(consented_at__isnull=False),
                    then=Value(self.model.IN_PROGRESS)
                ),
                default=Value(self.model.NOT_STARTED),
                output_field=CharField()
            )
        )


class SurveyResponseManager(models.Manager):
    """Survey Response model manager."""

    def get_queryset(self):
        return SurveyResponseQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def with_status(self):
        return self.get_queryset().with_status()
