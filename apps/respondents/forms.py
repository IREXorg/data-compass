from django import forms
from django.utils.translation import ugettext_lazy as _

from mptt.forms import TreeNodeChoiceField

from .models import Respondent


class RespondentConsentForm(forms.Form):
    consented = forms.BooleanField(
        label=_('I have read and understand the information above.'),
        required=True,
        initial=True,
        widget=forms.HiddenInput()
    )

    def clean_consented(self):
        data = self.cleaned_data['consented']
        if not data:
            raise forms.ValidationError(_('Consent must be provided to continue'), code='invalid')

        return data


class RespondentForm(forms.ModelForm):
    hierarchy_level = TreeNodeChoiceField(queryset=None)

    class Meta:
        model = Respondent
        fields = ['first_name', 'last_name', 'email', 'gender', 'hierarchy_level', 'role']

    def __init__(self, survey=None, project=None, *args, **kwargs):

        if not survey:
            raise ValueError(_(f'Survey must be specified to initialize {self.__class__.__name__}'))

        # get project inorder to limit hierarchy_level choices
        if not project:
            project = survey.project
        elif not project:
            raise ValueError(_(f'Project or Survey must be specified to initialize {self.__class__.__name__}'))

        super().__init__(*args, **kwargs)

        if 'hierarchy_level' in self.fields:
            self.fields['hierarchy_level'].queryset = project.hierarchy_levels.all()
        if 'hierarchy' in self.fields:
            self.fields['hierarchy'].queryset = project.hierarchies.all()
        if 'gender' in self.fields:
            self.fields['gender'].queryset = survey.genders.all()
        self.fields['role'].queryset = survey.roles.all()


class ResponseRespondentForm(RespondentForm):

    class Meta:
        model = Respondent
        fields = ['first_name', 'last_name', 'email', 'gender', 'hierarchy', 'role']
        labels = {
            'first_name': _('What is your first name?'),
            'last_name': _('What is your last name?'),
            'email': _('What is your email address?'),
            'gender': _('What is your gender?'),
            'role': _('What is your role at your organization?'),
        }
        widgets = {
            'hierarchy': forms.HiddenInput
        }

    def __init__(self, survey=None, project=None, *args, **kwargs):
        super().__init__(survey=survey, project=project, *args, **kwargs)
        self.fields.pop('hierarchy_level', None)

        for field_name, field in self.fields.items():
            field.required = True

        if not survey.allow_collect_email:
            self.fields.pop('email', None)

        if not survey.allow_collect_name:
            self.fields.pop('first_name', None)
            self.fields.pop('last_name', None)

        if not survey.allow_collect_gender:
            self.fields.pop('gender', None)

        self.fields['hierarchy'].queryset = project.hierarchies.all()


class RespondentCreateInviteForm(forms.Form):
    survey = forms.CharField()
    project = forms.CharField()
    respondent = forms.MultipleChoiceField(required=True)


class RespondentSendInviteForm(forms.Form):
    survey = forms.CharField(required=True)
    respondents = forms.MultipleChoiceField(required=True)
