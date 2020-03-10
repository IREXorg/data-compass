from django import forms
from django.forms import ModelForm

from ..models import Topic


class TopicCreateForm(ModelForm):
    """
    Basic Topic create form

    TODO: remove survey once in topic context
    """

    class Meta:
        model = Topic
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
        model = Topic
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2})
        }
