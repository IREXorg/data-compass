"""
This module holds strings likely from third-party dependencies that need to
be translated within scope of this project.
"""

from django.utils.translation import gettext_lazy as _

strings = {
    _('E-mail'),
    _('Remember Me'),
    _('E-mail address'),
    _('The e-mail address and/or password you specified are not correct.'),
    _('The e-mail address is not assigned to any user account'),
    _('You must type the same password each time.'),
    _('Password (again)'),
    _('A user is already registered with this e-mail address.')
}
