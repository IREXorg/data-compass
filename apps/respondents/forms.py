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
        self.fields['hierarchy_level'].queryset = project.hierarchy_levels.all()
        self.fields['role'].queryset = survey.roles.all()
