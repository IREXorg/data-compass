from django.conf import settings
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


@receiver(post_save, sender=Survey)
def add_survey_dataset_frequencies(sender, instance, created, **kwargs):
    """
    Add default dataset frequencies if a new survey instance is created.
    """

    if created:
        for frequency in settings.SURVEYS_DEFAULT_DATASET_FREQUENCIES:
            instance.dataset_frequencies.create(name=frequency)


@receiver(post_save, sender=Survey)
def add_survey_dataset_access(sender, instance, created, **kwargs):
    """
    Add default dataset access options if a new survey instance is created.
    """

    if created:
        for access in settings.SURVEYS_DEFAULT_DATASET_ACCESS:
            instance.dataset_access.create(name=access)
