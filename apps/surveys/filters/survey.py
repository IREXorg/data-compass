from django.utils.translation import ugettext_lazy as _

import django_filters

from core.mixins import SearchVectorFilterMixin

from ..models import Survey


class SurveyListFilter(SearchVectorFilterMixin, django_filters.FilterSet):
    """
    Surveys list filters
    """
    name = django_filters.CharFilter(lookup_expr='icontains')
    display_name = django_filters.CharFilter(lookup_expr='icontains')

    q = django_filters.CharFilter(
        label=_('Search text'),
        method='filter_search_vector',
    )

    search_vector_fields = ['name', 'display_name']

    class Meta:
        model = Survey
        fields = ('q', 'name', 'display_name')
