from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from ..models import Entity


class EntityCreateForm(ModelForm):
    """
    Basic Entity create form
    """

    class Meta:
        model = Entity
        fields = ['survey', 'name', 'hierarchy']
        widgets = {
            'survey': forms.HiddenInput(),
        }
        labels = {
            'name': _('Entity Name'),
            'hierarchy': _('System Hierarchy Level'),
        }

    def __init__(self, survey=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if survey:
            self.initial['survey'] = survey


class EntityUpdateForm(ModelForm):
    """
    Basic Entity update form
    """
    class Meta:
        model = Entity
        fields = ['name', 'hierarchy']
        widgets = {}
        labels = {
            'name': _('Entity Name'),
            'hierarchy': _('System Hierarchy Level'),
        }
