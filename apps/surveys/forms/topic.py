from django import forms
from django.forms import ModelForm

from ..models import Dataset


class TopicCreateForm(ModelForm):
    """
    Basic Topic create form
    """

    class Meta:
        model = Dataset  # TODO: restore to Topic
        fields = ['survey', 'name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
            'survey': forms.HiddenInput(),
        }

    def __init__(self, survey=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if survey:
            self.initial['survey'] = survey


class TopicUpdateForm(ModelForm):
    """
    Basic Topic update form
    """
    class Meta:
        model = Dataset  # TODO: restore to Topic
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2})
        }
