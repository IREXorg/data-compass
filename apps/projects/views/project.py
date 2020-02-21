# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.urls import reverse_lazy as reverse
from django.utils.translation import ugettext_lazy as _
# from django.views.generic.detail import DetailView
# from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from core.mixins import PageTitleMixin

# from ..filters import SurveyListFilter
# from ..forms import SurveyCreateForm, SurveyUpdateForm
# from ..mixins import SurveyCreatorMixin
from ..models import Project


class ProjectListView(ListView):
    """
    List projects view.

    Allow current signin user to view list of allowed projects.

    **Example request**:

    .. code-block:: http

        GET  /project/
    """

    # Translators: This is projects list page title
    page_title = _('Project List')
    template_name = 'projects/project_list.html'
    list_view_name = 'projects/project_list.html'
    model = Project
    context_object_name = 'projects'
    # filterset_class = ProjectListFilter
    queryset = Project.objects.all()
    ordering = ['created_at']
    paginate_by = 10
