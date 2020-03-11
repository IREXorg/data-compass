from apps.projects.models import Project

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
