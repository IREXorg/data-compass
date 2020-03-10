from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from ..models import Survey

# from django_summernote.widgets import SummernoteInplaceWidget


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
    Survey edit step one form
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


class SurveyEditStepTwoForm(ModelForm):
    """
    Survey edit step two form
    """
    class Meta:
        model = Survey
        fields = ['allow_respondent_topics', 'respondent_topic_number']
        widgets = {
            'allow_respondent_topics': forms.RadioSelect(),
        }
        labels = {
            'allow_respondent_topics': _('Allow respondents to enter their own value here'),
            'respondent_topic_number': _('How many topics would you like Respondents to select?. They will complete the entire survey for each topic.'),  # noqa: E501
        }


class SurveyEditStepThreeForm(ModelForm):
    """
    Survey edit step three form
    """
    class Meta:
        model = Survey
        fields = ['allow_respondent_datasets']
        widgets = {
            'allow_respondent_datasets': forms.RadioSelect(),
        }
        labels = {
            'allow_respondent_datasets': _('Allow users to add their own options(not recommended)'),
        }


class SurveyEditStepFourForm(ModelForm):
    """
    Survey edit step four form
    """
    class Meta:
        model = Survey
        fields = ['allow_respondent_entities']
        widgets = {
            'allow_respondent_entities': forms.RadioSelect(),
        }
        labels = {
            'allow_respondent_entities': _('Allow respondents to enter their own value here'),
        }


class SurveyEditStepFiveForm(ModelForm):
    """
    Survey edit step five form
    """
    class Meta:
        model = Survey
        fields = ['allow_respondent_storages']
        widgets = {
            'allow_respondent_storages': forms.RadioSelect(),
        }
        labels = {
            'allow_respondent_storages': _('Allow users to enter their own value here'),
        }


class SurveyEditStepSixForm(ModelForm):
    """
    Survey edit step six form
    """
    class Meta:
        model = Survey
        fields = ['introduction_text', 'closing_text']
        widgets = {
            'introduction_text': forms.Textarea(attrs={'rows': 2}),
            'closing_text': forms.Textarea(attrs={'rows': 2}),
        }
        labels = {
            'introduction_text': _('Introduction text:'),
            'closing_text': _('Closing text:'),
        }
