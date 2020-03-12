from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from ..models import Respondent


class RespondentCreateForm(ModelForm):
    """
    Basic Respondent create form
    """

    class Meta:
        model = Respondent
        fields = ['survey', 'email', 'hierarchy']
        widgets = {
            'survey': forms.HiddenInput(),
        }
        labels = {
            'email': _('Email address'),
            'hierarchy': _('System hierarchy Level'),
        }

    def __init__(self, survey=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['hierarchy'].required = True
        if survey:
            self.initial['survey'] = survey


class RespondentUpdateForm(ModelForm):
    """
    Basic Respondent update form
    """
    class Meta:
        model = Respondent
        fields = ['email', 'hierarchy']
        widgets = {}
        labels = {
            'email': _('Email address'),
            'hierarchy': _('System hierarchy Level'),
        }
