from django.db import models
from django.utils.translation import ugettext_lazy as _


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created_at`` and ``modified_at`` fields.
    """
    created_at = models.DateTimeField(
        _('created at'),
        auto_now_add=True,
        db_index=True
    )
    modified_at = models.DateTimeField(
        _('modified at'),
        auto_now=True,
        db_index=True
    )

    class Meta:
        abstract = True
