import django_filters

from .models import Project


class ProjectListFilter(django_filters.FilterSet):
    """
    Project list filters
    """
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Project
        fields = ['name', 'created_at']
