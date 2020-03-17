from django.utils.translation import ugettext_lazy as _

import django_filters

from core.mixins import SearchVectorFilterMixin

from .models import Project


class ProjectListFilter(SearchVectorFilterMixin, django_filters.FilterSet):
    """
    Project list filters
    """
    name = django_filters.CharFilter(lookup_expr='icontains')

    q = django_filters.CharFilter(
        label=_('Search text'),
        method='filter_search_vector',
    )

    search_vector_fields = ['name']

    class Meta:
        model = Project
        fields = ['q', 'name', 'created_at']
