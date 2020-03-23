from django import forms
from django.forms import ModelForm

from ..models import Logo


class LogoCreateForm(ModelForm):
    """
    Basic Logo create form
    """

    class Meta:
        model = Logo
        fields = ['survey', 'name', 'image']
        widgets = {
            'survey': forms.HiddenInput(),
        }

    def __init__(self, survey=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = True
        if survey:
            self.initial['survey'] = survey


class LogoUpdateForm(ModelForm):
    """
    Basic Logo update form
    """
    class Meta:
        model = Logo
        fields = ['name', 'image']
        widgets = {}
