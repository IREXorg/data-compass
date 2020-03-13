import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from django_countries.fields import CountryField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from phonenumber_field.modelfields import PhoneNumberField

from core.models import TimeStampedModel

from .managers import GenderManager


class Gender(TimeStampedModel):
    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    name = models.CharField(_('name'), max_length=50)
    code = models.SlugField(_('code'), max_length=255, blank=True, unique=True)
    is_primary = models.BooleanField(
        _('is primary'),
        default=False,
        blank=True,
        help_text=_('Shared system wide. Not for specific project or survey only.')
    )

    objects = GenderManager()

    class Meta:
        verbose_name = _('Gender')
        verbose_name_plural = _('Gender')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = slugify(self.name)
        super().save(*args, **kwargs)


class User(AbstractUser):
    _ADMINISTRATOR = _('administrator')
    _FACILITATOR = _('facilitator')
    _RESPONDENT = _('respondent')

    uuid = models.UUIDField(
        _('UUID'),
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    avatar = models.ImageField(
        _('profile picture'),
        blank=True,
        null=True,
        upload_to='users/avatars'
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
    phone_number = PhoneNumberField(_('phone number'), blank=True)
    gender = models.ForeignKey(
        'users.Gender',
        blank=True,
        null=True,
        related_name='users',
        related_query_name='user',
        on_delete=models.SET_NULL,
        verbose_name=_('gender')
    )
    country = CountryField(_('country'), blank=True)
    address = models.TextField(_('address'), blank=True)
    is_facilitator = models.BooleanField(_('is facilitator'), default=False)
    is_respondent = models.BooleanField(_('is respondent'), default=False)

    @property
    def user_type(self):
        titles = []

        # NOTE: Calling str() on translatable/proxy string so that they can be joined as normal strings.
        if self.is_staff:
            titles.append(str(self._ADMINISTRATOR))
        if self.is_facilitator:
            titles.append(str(self._FACILITATOR))
        if self.is_respondent:
            titles.append(str(self._RESPONDENT))

        return ', '.join(titles)
