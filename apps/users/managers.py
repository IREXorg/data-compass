from django.db import models


class GenderQuerySet(models.QuerySet):
    """Gender Queryset."""

    def primary(self):
        """Returns a queryset of primary gender objects."""
        return self.filter(is_primary=True)


class GenderManager(models.Manager):
    """Gender model manager."""

    def get_queryset(self):
        return GenderQuerySet(self.model, using=self._db)

    def primary(self):
        return self.get_queryset().primary()
