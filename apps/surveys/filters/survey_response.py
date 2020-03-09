from django import forms
from django.utils.translation import ugettext_lazy as _

import django_filters

from ..models import Response as SurveyResponse
from .base import facilitator_projects, facilitator_surveys


class SurveyResponseFilter(django_filters.FilterSet):

    project = django_filters.ModelChoiceFilter(
        field_name='survey__project',
        queryset=facilitator_projects,
        label=_('Project'),
    )

    survey = django_filters.ModelChoiceFilter(
        field_name='survey',
        queryset=facilitator_surveys,
    )

    status = django_filters.MultipleChoiceFilter(
        choices=SurveyResponse.STATUS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label=_('Status')
    )

    class Meta:
        model = SurveyResponse
        fields = ['project', 'survey', 'respondent__email']
