from django import forms
from django.forms import ModelForm
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from apps.users.models import Gender

from ..models import Survey


class GenderCreateForm(ModelForm):
    """
    Basic Gender create form
    """
    survey = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Gender
        fields = ['survey', 'name']
        widgets = {}
        labels = {
            'name': _('Gender Name'),
        }

    def __init__(self, survey=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if survey:
            self.initial['survey'] = survey.pk

    def save(self, commit=True):
        # check if already exists
        name = self.cleaned_data.get('name')
        code = slugify(name)
        gender = Gender.objects.filter(code=code).first()

        # create new gender
        if not gender:
            gender = super().save(commit=commit)

        # link gender to survey
        survey_pk = self.cleaned_data.get('survey')
        survey = Survey.objects.get(pk=survey_pk)
        survey.genders.add(gender)

        return gender


class GenderUpdateForm(ModelForm):
    """
    Basic Gender update form
    """
    class Meta:
        model = Gender
        fields = ['name']
        widgets = {}
        labels = {
            'name': _('Gender Name'),
        }
