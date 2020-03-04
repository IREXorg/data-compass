from django import forms
# from django.conf import settings
from django.forms import ModelForm

from ..models import Survey


class SurveyCreateForm(ModelForm):
    """
    Basic Survey create form

    TODO: remove project once in project context
    """
    # languages = forms.MultipleChoiceField(choices=settings.LANGUAGES),

    class Meta:
        model = Survey
        fields = ['project', 'name', 'description', 'display_name', 'research_question', 'languages']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
            'project': forms.HiddenInput(),
            'languages': forms.CheckboxSelectMultiple()
        }

    def __init__(self, project=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['languages'] = forms.MultipleChoiceField(
        #     widget=forms.CheckboxSelectMultiple(),
        #     choices=settings.LANGUAGES
        #     ),
        if project:
            self.initial['project'] = project


class SurveyUpdateForm(ModelForm):
    """
    Basic Survey update form
    """
    class Meta:
        model = Survey
        fields = ['name', 'description', 'display_name', 'research_question', 'languages']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
            'languages': forms.CheckboxSelectMultiple(),
            # 'languages': forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), choices=settings.LANGUAGES),
        }
