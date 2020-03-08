from django import forms
from django.utils.translation import ugettext_lazy as _

import django_filters

from apps.projects.models import Project

from ..models import Response as SurveyResponse
from ..models import Survey


def facilitator_projects(request):
    """Return a queryset of projects facilitated by user."""
    if not request.user.is_authenticated:
        return Project.objects.none()

    return Project.objects.filter(facilitators=request.user)


def facilitator_surveys(request):
    """Return a queryset of surveys facilitated by user."""
    if not request.user.is_authenticated:
        return Survey.objects.none()

    return Survey.objects.filter(project__facilitators=request.user)


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
