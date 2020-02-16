import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_countries.fields import CountryField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from phonenumber_field.modelfields import PhoneNumberField


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
        _('avatar'),
        blank=True,
        null=True,
        upload_to='users/avatars'
    )
    avatar_thumbnail = ImageSpecField(
        source='avatar',
        processors=[ResizeToFit(100, 100)],
        format='JPEG',
        options={'quality': 100}
    )
    phone_number = PhoneNumberField(_('phone number'), blank=True)
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
