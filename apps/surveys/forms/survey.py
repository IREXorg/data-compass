from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

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
            'project': forms.HiddenInput(),
            'languages': forms.CheckboxSelectMultiple()
        }

    def __init__(self, project=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        }


class SurveyEditStepOneForm(ModelForm):
    """
    Survey update step one form
    """
    class Meta:
        model = Survey
        fields = ['login_required', 'respondent_can_aggregate', 'respondent_can_invite']
        widgets = {
            'login_required': forms.RadioSelect(),
            'respondent_can_aggregate': forms.RadioSelect(),
            'respondent_can_invite': forms.RadioSelect()
        }
        labels = {
            'login_required': _('Do you want the survey to be taken by invited users only?'),
            'respondent_can_aggregate':
                _("Do you want repondents to see visualizations or aggregates of other users' responses?"),
            'respondent_can_invite': _('Do you want users to share email addresses of other potential respondents?'),
        }
