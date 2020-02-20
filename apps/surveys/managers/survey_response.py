from django.db import models


class SurveyResponseQuerySet(models.QuerySet):

    def active(self):
        """Returns a queryset of active survey responses."""
        return self.filter(survey__is_active=True)


class SurveyResponseManager(models.Manager):
    """Survey Response model manager."""

    def get_queryset(self):
        return SurveyResponseQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()
