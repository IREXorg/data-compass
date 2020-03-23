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
        fields = ['survey', 'name', 'hierarchy_level']
        widgets = {
            'survey': forms.HiddenInput(),
        }
        labels = {
            'name': _('Entity Name'),
            'hierarchy_level': _('System Hierarchy Level'),
        }

    def __init__(self, survey=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if survey:
            self.initial['survey'] = survey
            self.fields['hierarchy_level'].queryset = survey.project.hierarchy_levels.all()


class EntityUpdateForm(ModelForm):
    """
    Basic Entity update form
    """
    class Meta:
        model = Entity
        fields = ['name', 'hierarchy_level']
        widgets = {}
        labels = {
            'name': _('Entity Name'),
            'hierarchy_level': _('System Hierarchy Level'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hierarchy_level'].queryset = self.instance.survey.project.hierarchy_levels.all()
