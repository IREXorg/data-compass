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
        fields = ['survey', 'name', 'hierarchy_level']
        widgets = {
            'survey': forms.HiddenInput(),
        }
        labels = {
            'name': _('Role Name'),
            'hierarchy_level': _('System Hierarchy Level'),
        }

    def __init__(self, survey=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if survey:
            self.initial['survey'] = survey
            self.fields['hierarchy_level'].queryset = survey.project.hierarchy_levels.all()


class RoleUpdateForm(ModelForm):
    """
    Basic Role update form
    """
    class Meta:
        model = Role
        fields = ['name', 'hierarchy_level']
        widgets = {}
        labels = {
            'name': _('Role Name'),
            'hierarchy_level': _('System Hierarchy Level'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hierarchy_level'].queryset = self.instance.survey.project.hierarchy_levels.all()
