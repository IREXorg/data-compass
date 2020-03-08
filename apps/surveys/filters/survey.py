import django_filters

from ..models import Survey


class SurveyListFilter(django_filters.FilterSet):
    """
    Surveys list filters
    """
    name = django_filters.CharFilter(lookup_expr='icontains')
    display_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Survey
        fields = ('name', 'display_name')
