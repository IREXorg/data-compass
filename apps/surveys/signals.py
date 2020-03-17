from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Survey


@receiver(post_save, sender=Survey)
def add_primary_survey_gender(sender, instance, created, **kwargs):
    """
    If a new instance is created and instance has no genders
    assign instance with primary genders.
    """

    if created and not instance.genders.exists():
        instance.genders.add(*instance.genders.model.objects.primary())
