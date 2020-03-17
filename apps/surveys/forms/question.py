from django import forms
from django.forms import ModelForm

from ..models import Question


class QuestionCreateForm(ModelForm):
    """
    Basic Question create form
    """

    class Meta:
        model = Question
        fields = ['survey', 'label', 'type']
        widgets = {
            'label': forms.Textarea(attrs={'rows': 2}),
            'survey': forms.HiddenInput(),
        }

    def __init__(self, survey=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if survey:
            self.initial['survey'] = survey


class QuestionUpdateForm(ModelForm):
    """
    Basic Question update form
    """
    class Meta:
        model = Question
        fields = ['label', 'type']
        widgets = {
            'label': forms.Textarea(attrs={'rows': 2})
        }
