from django.db import models


class SurveyQuerySet(models.QuerySet):

    def active(self):
        """
        Returns a queryset of active surveys.
        """
        return self.filter(is_active=True)


class SurveyManager(models.Manager):
    """Survey model manager."""

    def get_queryset(self):
        return SurveyQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()
