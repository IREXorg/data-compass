from django.db import models


class RespondentQuerySet(models.QuerySet):

    def active(self):
        """
        Returns a queryset of active respondents.

        Active respondents includes respondents with active surveys.
        """
        return self.filter(survey__is_active=True)


class RespondentManager(models.Manager):
    """Respondent model manager."""

    def get_queryset(self):
        return RespondentQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()
