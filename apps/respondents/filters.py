from distutils.util import strtobool

from django import forms
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _

import django_filters

from apps.users.models import Gender
from core.filters import facilitator_projects, facilitator_surveys
from core.mixins import SearchVectorFilterMixin

from .models import Respondent


class RespondentFilter(SearchVectorFilterMixin, django_filters.FilterSet):
    REGISTERED = 1
    NOT_REGISTERED = 0

    REGISTERED_CHOICES = (
        (REGISTERED, pgettext_lazy('users', 'Registered')),
        (NOT_REGISTERED, pgettext_lazy('users', 'Not registered')),
    )

    q = django_filters.CharFilter(
        label=_('Search text'),
        method='filter_search_vector',
    )

    gender = django_filters.ModelMultipleChoiceFilter(
        queryset=Gender.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    status = django_filters.MultipleChoiceFilter(
        choices=Respondent.STATUS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label=_('Status')
    )

    registered = django_filters.TypedMultipleChoiceFilter(
        choices=REGISTERED_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label=_('Registration status'),
        coerce=strtobool
    )

    project = django_filters.ModelChoiceFilter(
        field_name='survey__project',
        queryset=facilitator_projects,
        label=_('Project'),
    )

    survey = django_filters.ModelChoiceFilter(
        field_name='survey',
        queryset=facilitator_surveys,
    )

    search_vector_fields = ['first_name', 'last_name', 'email']

    class Meta:
        model = Respondent
        fields = ['q', 'gender', 'status', 'registered', 'project', 'survey']
