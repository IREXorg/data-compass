import uuid

from django.conf import settings
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from django_countries.fields import CountryField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from phonenumber_field.modelfields import PhoneNumberField

from core.models import TimeStampedModel


class Organization(TimeStampedModel):
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
    phone_number = PhoneNumberField(_('phone number'), blank=True)
    email = models.EmailField(_('email'), blank=True)
    avatar = models.ImageField(
        _('avatar'),
        blank=True,
        null=True,
        upload_to='organizations/avatars'
    )
    avatar_thumbnail = ImageSpecField(
        source='avatar',
        processors=[ResizeToFit(100, 100)],
        format='PNG',
        options={'quality': 100}
    )
    avatar_sm = ImageSpecField(
        source='avatar',
        processors=[ResizeToFit(50, 50)],
        format='PNG',
        options={'quality': 100}
    )
    website = models.URLField(_('website'), blank=True)
    country = CountryField(_('country'), blank=True)
    address = models.TextField(_('address'), blank=True)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('members'),
        related_name='organizations',
        related_query_name='organization',
        blank=True
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
        related_name='created_organizations',
        related_query_name='created_organization',
        on_delete=models.CASCADE
    )
    extras = JSONField(_('extras'), blank=True, default=dict)

    class Meta:
        verbose_name = _('Organization')
        verbose_name_plural = _('Organizations')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = slugify(self.name[:50])
        super().save(*args, **kwargs)
