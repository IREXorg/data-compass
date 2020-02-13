from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from ..forms import SurveyForm
from ..models import Survey


class SurveyListView(ListView):
    model = Survey
    paginate_by = 20


class SurveyCreateView(CreateView):
    model = Survey
    form_class = SurveyForm
    success_url = reverse_lazy('surveys:survey-list')


class SurveyDetailView(DetailView):
    model = Survey


class SurveyUpdateView(UpdateView):
    model = Survey
    form_class = SurveyForm
    success_url = reverse_lazy('surveys:survey-list')


class SurveyDeleteView(DeleteView):
    model = Survey
    success_url = reverse_lazy('surveys:survey-list')
