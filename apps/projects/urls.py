from django.urls import path

from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='project-list'),
    path('create', views.ProjectCreateView.as_view(), name='project-create'),
]
