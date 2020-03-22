from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from django_summernote.widgets import SummernoteWidget

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


class SurveyUnpublishForm(ModelForm):
    """
    Basic Survey unpublish form
    """
    class Meta:
        model = Survey
        fields = []
        widgets = {}


class SurveyPublishForm(ModelForm):
    """
    Basic Survey publish form
    """
    class Meta:
        model = Survey
        fields = []
        widgets = {}


class SurveyEditStepOneForm(ModelForm):
    """
    Survey edit step one form
    """
    class Meta:
        model = Survey
        fields = [
            'allow_respondent_hierarchy_levels', 'dont_link_hierarchy_levels',
            'login_required', 'invitation_required',
            'respondent_can_aggregate', 'respondent_can_invite'
        ]
        widgets = {
            'allow_respondent_hierarchy_levels': forms.RadioSelect(),
            'dont_link_hierarchy_levels': forms.RadioSelect(),
            'login_required': forms.RadioSelect(),
            'invitation_required': forms.RadioSelect(),
            'respondent_can_aggregate': forms.RadioSelect(),
            'respondent_can_invite': forms.RadioSelect()
        }
        labels = {
            'allow_respondent_hierarchy_levels': _('Allow respondents to add to Lists?'),
            'dont_link_hierarchy_levels': _('Do not link respondents with system hierarchy levels?'),
            'login_required': _('Do you want these users to log in before responding to the survey?'),
            'invitation_required': _('Do you want the survey to be taken by invited users only?'),
            'respondent_can_aggregate': _(
                "Do you want repondents to see visualizations or aggregates "
                "of other users' responses?"
            ),
            'respondent_can_invite': _(
                'Do you want users to share email '
                'addresses of other potential respondents?'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.required = True


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
            'allow_respondent_topics': _('Allow respondents to enter their own value here?'),
            'respondent_topic_number': _(
                'What is the maximum number of topics you would like '
                'Respondents to select? They will complete the entire '
                'survey for each topic they select.'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.required = True


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
            'allow_respondent_datasets': _('Allow users to add their own options?'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.required = True


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
            'allow_respondent_entities': _('Allow respondents to enter their own value here?'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.required = True


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
            'allow_respondent_storages': _('Allow users to enter their own value here?'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.required = True


class SurveyEditStepSixForm(ModelForm):
    """
    Survey edit step six form
    """
    class Meta:
        model = Survey
        fields = [
            'allow_collect_email', 'allow_collect_name',
            'allow_collect_gender', 'introduction_text', 'closing_text'
        ]
        widgets = {
            'introduction_text': SummernoteWidget(),
            'closing_text': SummernoteWidget(),
        }
        labels = {
            'introduction_text': _('Introduction text:'),
            'closing_text': _('Closing text:'),
        }
