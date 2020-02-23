from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy as reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from core.mixins import PageTitleMixin

from .filters import ProjectListFilter
from .forms import ProjectCreateForm, ProjectUpdateForm
from .mixins import ProjectCreatorMixin
from .models import Project


class ProjectListView(LoginRequiredMixin, PageTitleMixin, ListView):
    """
    List projects view.

    Allow current signin user to view list of allowed projects.

    **Example request**:

    .. code-block:: http

        GET  /projects/
    """

    # Translators: This is projects list page title
    page_title = _('Project List')
    template_name = 'projects/project_list.html'
    list_view_name = 'projects/project_list.html'
    model = Project
    context_object_name = 'projects'
    filterset_class = ProjectListFilter
    queryset = Project.objects.all()
    ordering = ['created_at']
    paginate_by = 10


class ProjectCreateView(LoginRequiredMixin, ProjectCreatorMixin, PageTitleMixin, CreateView):
    """
    Create project view.

    Allow current signin user to create a new project and redirect to
    projects list page.

    **Example request**:

    .. code-block:: http

        POST /projects/create
    """

    # Translators: This is projects list page title
    page_title = _('Create Project')
    template_name = 'projects/project_create.html'
    model = Project
    form_class = ProjectCreateForm
    success_url = reverse('projects:project-list')


class ProjectDetailView(LoginRequiredMixin, PageTitleMixin, DetailView):
    """
    View project details view.

    Allow current signin user to view project details.

    **Example request**:

    .. code-block:: http

        GET  /projects/1234567890
    """

    # Translators: This is project view page title
    page_title = _('View Project')
    template_name = 'projects/project_detail.html'
    model = Project


class ProjectUpdateView(LoginRequiredMixin, ProjectCreatorMixin, PageTitleMixin, UpdateView):
    """
    Update project details view.

    Allow current signin user to update existing project details and
    redirect to project list page.

    **Example request**:

    .. code-block:: http

        PUT  /projects/1234567890/update
    """

    # Translators: This is project update page title
    page_title = _('Update project')
    template_name = 'projects/project_update.html'
    model = Project
    form_class = ProjectUpdateForm
    success_url = reverse('projects:project-list')


class ProjectDeleteView(LoginRequiredMixin, PageTitleMixin, DeleteView):
    """
    Delete project details

    Allow current signin user to delete existing project and
    redirect to project list page.

    **Example request**:

    .. code-block:: http

        DELETE  /projects/1234567890/delete
    """

    # Translators: This is project delete page title
    page_title = _('Delete Project')
    template_name = 'projects/project_delete.html'
    model = Project
    success_url = reverse('projects:project-list')
