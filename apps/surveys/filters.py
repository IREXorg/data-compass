from distutils.util import strtobool

from django import forms
from django.contrib.postgres.search import SearchVector
from django.utils.translation import ugettext_lazy as _

import django_filters

from apps.users.models import Gender

from .models import Respondent, Survey


class SurveyListFilter(django_filters.FilterSet):
    """
    Surveys list filters
    """
    name = django_filters.CharFilter(lookup_expr='icontains')
    display_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Survey
        fields = ('name', 'display_name')


class RespondentFilter(django_filters.FilterSet):
    REGISTERED = 1
    NOT_REGISTERED = 0

    REGISTERED_CHOICES = (
        (REGISTERED, _('Registered')),
        (NOT_REGISTERED, _('Not registered')),
    )

    q = django_filters.CharFilter(
        label=_('Search text'),
        method='filter_q',
        widget=forms.HiddenInput,
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

    class Meta:
        model = Respondent
        fields = ['gender', 'status', 'registered', 'survey__project', 'survey']

    def filter_q(self, queryset, name, value):
        # TODO: Create Index to avoid performance issues
        # https://docs.djangoproject.com/en/3.0/ref/contrib/postgres/search/#performance

        if not value:
            return queryset

        return queryset.annotate(
            search_vector=SearchVector('first_name', 'last_name', 'email')
        ).filter(search_vector=value)
