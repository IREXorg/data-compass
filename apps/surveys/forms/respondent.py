from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from apps.respondents.models import Respondent
from apps.users.models import User


class RespondentCreateForm(ModelForm):
    """
    Basic Respondent create form
    """

    class Meta:
        model = Respondent
        fields = ['survey', 'email', 'hierarchy_level']
        widgets = {
            'survey': forms.HiddenInput(),
        }
        labels = {
            'email': _('Email address'),
            'hierarchy_level': _('System hierarchy Level'),
        }

    def __init__(self, survey=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['hierarchy_level'].required = True
        if survey:
            self.initial['survey'] = survey
            self.fields['hierarchy_level'].queryset = survey.project.hierarchy_levels.all()

    def save(self, commit=True):
        respondent = super().save(commit=commit)

        # link respondent with user if exists
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            respondent.user = user
            respondent.save()

        return respondent


class RespondentUpdateForm(ModelForm):
    """
    Basic Respondent update form
    """
    class Meta:
        model = Respondent
        fields = ['email', 'hierarchy_level']
        widgets = {}
        labels = {
            'email': _('Email address'),
            'hierarchy_level': _('System hierarchy Level'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['hierarchy_level'].required = True
        self.fields['hierarchy_level'].queryset = self.instance.survey.project.hierarchy_levels.all()

    def save(self, commit=True):
        respondent = super().save(commit=commit)

        # link respondent with user if exists
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            respondent.user = user
            respondent.save()

        return respondent
