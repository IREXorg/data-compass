from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy as reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from django_filters.views import FilterView

from apps.surveys.models import Survey
from core.mixins import PageMixin

from .filters import ProjectListFilter
from .forms import ProjectCreateForm, ProjectUpdateForm
from .mixins import ProjectCreatorMixin, ProjectFacilitatorMixin
from .models import Project


class ProjectListView(ProjectFacilitatorMixin, PageMixin, FilterView):
    """
    List projects view.

    Allow current signin user to view list of allowed projects.

    **Example request**:

    .. code-block:: http

        GET  /projects/
    """

    # Translators: This is projects list page title
    page_title = _('My Projects')
    template_name = 'projects/project_list.html'
    list_view_name = 'projects/project_list.html'
    model = Project
    context_object_name = 'projects'
    filterset_class = ProjectListFilter
    queryset = Project.objects.all()
    ordering = ['created_at']
    paginate_by = 10


class ProjectCreateView(SuccessMessageMixin, ProjectFacilitatorMixin, ProjectCreatorMixin, PageMixin, CreateView):
    """
    Create project view.

    Allow current signed in user to create a new project and redirect to
    projects detail page.

    **Example request**:

    .. code-block:: http

        POST /projects/create
    """

    # Translators: This is projects list page title
    page_title = _('Create a project')
    template_name = 'projects/project_create.html'
    context_object_name = 'project'
    model = Project
    form_class = ProjectCreateForm
    success_message = _('Project was created successfully')

    def get_success_url(self):
        """
        Returns project edit URL as success URL.

        Update URL is returned instead of detail URL to allow user to
        preview the created hierarchy.
        """
        return reverse('projects:project-update', kwargs={'pk': self.object.pk})


class ProjectDetailView(ProjectFacilitatorMixin, PageMixin, DetailView):
    """
    View project details view.

    Allow current signin user to view project details.

    **Example request**:

    .. code-block:: http

        GET  /projects/1234567890
    """

    # Translators: This is project view page title
    page_title = _('View a project')
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'
    model = Project

    def get_surveys(self):
        """Get allowed surveys for a user project"""
        # TODO filter by user
        return Survey.objects.filter(project=self.object)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['surveys'] = self.get_surveys()
        return context

    def get_page_title(self):
        """Prvide page_title."""
        return self.object.name


class ProjectUpdateView(SuccessMessageMixin, ProjectFacilitatorMixin, PageMixin, UpdateView):
    """
    Update project details view.

    Allow current signin user to update existing project details and
    redirect to project list page.

    **Example request**:

    .. code-block:: http

        PUT  /projects/1234567890/update
    """

    # Translators: This is project update page title
    page_title = _('Update a project')
    template_name = 'projects/project_update.html'
    context_object_name = 'project'
    model = Project
    form_class = ProjectUpdateForm
    success_url = reverse('projects:project-list')
    success_message = _('Project was updated successfully')

    def get_form_kwargs(self):
        """
        Add request form class initialization arguments to help identifying hierarchy creator
        """
        form_kwargs = super().get_form_kwargs()
        form_kwargs['user'] = self.request.user
        return form_kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dataflow_hierarchy'] = self.object.hierarchies.all()
        return context


class ProjectDeleteView(SuccessMessageMixin, ProjectFacilitatorMixin, PageMixin, DeleteView):
    """
    Delete project details

    Allow current signin user to delete existing project and
    redirect to project list page.

    **Example request**:

    .. code-block:: http

        DELETE  /projects/1234567890/delete
    """

    # Translators: This is project delete page title
    page_title = _('Delete a project')
    template_name = 'projects/project_delete.html'
    context_object_name = 'project'
    model = Project
    success_message = _('Project was deleted successfully')
    success_url = reverse('projects:project-list')
