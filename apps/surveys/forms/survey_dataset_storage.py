from django import forms
from django.forms import ModelForm

from ..models import DatasetStorage


class DatasetStorageCreateForm(ModelForm):
    """
    Basic DatasetStorage create form
    """

    class Meta:
        model = DatasetStorage
        fields = ['survey', 'name']
        widgets = {
            'survey': forms.HiddenInput(),
        }

    def __init__(self, survey=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if survey:
            self.initial['survey'] = survey


class DatasetStorageUpdateForm(ModelForm):
    """
    Basic DatasetStorage update form
    """
    class Meta:
        model = DatasetStorage
        fields = ['name']
        widgets = {}
