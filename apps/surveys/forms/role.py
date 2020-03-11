from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from ..models import Role


class RoleCreateForm(ModelForm):
    """
    Basic Role create form
    """

    class Meta:
        model = Role
        fields = ['survey', 'name', 'hierarchy']
        widgets = {
            'survey': forms.HiddenInput(),
        }
        labels = {
            'name': _('Role Name'),
            'hierarchy': _('System Hierarchy Level'),
        }

    def __init__(self, survey=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if survey:
            self.initial['survey'] = survey


class RoleUpdateForm(ModelForm):
    """
    Basic Role update form
    """
    class Meta:
        model = Role
        fields = ['name', 'hierarchy']
        widgets = {}
        labels = {
            'name': _('Role Name'),
            'hierarchy': _('System Hierarchy Level'),
        }
