from django import forms
from django.forms import ModelForm

from ..models import Topic


class DatasetCreateForm(ModelForm):
    """
    Basic Dataset create form
    """

    class Meta:
        model = Topic  # TODO: restore to Dataset
        fields = ['survey', 'name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
            'survey': forms.HiddenInput(),
        }

    def __init__(self, survey=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if survey:
            self.initial['survey'] = survey


class DatasetUpdateForm(ModelForm):
    """
    Basic Dataset update form
    """
    class Meta:
        model = Topic  # TODO: restore to Dataset
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2})
        }
