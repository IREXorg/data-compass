from django.urls import path
from django.conf.urls import url


from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='project-list'),
    path('create', views.ProjectCreateView.as_view(), name='project-create'),
    url(r'^(?P<pk>\d+)/$', views.ProjectDetailView.as_view(), name='project-detail'),
    url(r'^(?P<pk>\d+)/update/$', views.ProjectUpdateView.as_view(), name='project-update'),

]
