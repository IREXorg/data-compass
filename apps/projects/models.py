import uuid

from django.conf import settings
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.urls import reverse_lazy as reverse
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from core.models import TimeStampedModel


class Project(TimeStampedModel):
    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    code = models.SlugField(
        _('code'),
        blank=True,
        allow_unicode=True,
        unique=True
    )
    organization = models.ForeignKey(
        'organizations.Organization',
        blank=True,
        null=True,
        related_name='projects',
        related_query_name='project',
        verbose_name=_('organization'),
        on_delete=models.SET_NULL
    )
    email = models.EmailField(_('email'), blank=True)
    phone_number = PhoneNumberField(_('phone number'), blank=True)
    avatar = models.ImageField(
        _('avatar'),
        blank=True,
        null=True,
        upload_to='organizations/avatars'
    )
    website = models.URLField(_('website'), blank=True)
    countries = ArrayField(
        CountryField(),
        verbose_name=_('countries'),
        blank=True,
        default=list
    )
    tags = ArrayField(
        models.CharField(max_length=50),
        verbose_name=_('tags'),
        blank=True,
        default=list
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('creator'),
        blank=True,
        related_name='created_projects',
        related_query_name='created_project',
        on_delete=models.CASCADE
    )
    extras = JSONField(_('extras'), blank=True, default=dict)

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        ordering = ['created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = slugify(self.name[:50])
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Obtain project absolute url."""
        return reverse('projects:project-detail', kwargs={'pk': self.pk})

    # Derive project name abbreviation
    @property
    def abbreviation(self):
        parts = []

        words = self.name.split(' ')
        for word in words:
            parts.append(str(word[0]))

        return ''.join(parts[:2])
