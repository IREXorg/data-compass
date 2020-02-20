from django import forms
from django.forms import ModelForm

from ..models import Survey


class SurveyCreateForm(ModelForm):
    """
    Basic Survey create form

    TODO: remove project once in project context
    """
    class Meta:
        model = Survey
        fields = ['project', 'name', 'description', 'display_name', 'research_question', 'languages']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }


class SurveyUpdateForm(ModelForm):
    """
    Basic Survey update form
    """
    class Meta:
        model = Survey
        fields = ['name', 'description', 'display_name', 'research_question', 'languages']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }
