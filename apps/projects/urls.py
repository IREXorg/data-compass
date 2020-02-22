from django.conf.urls import url


from . import views

app_name = 'projects'

urlpatterns = [
    url(r'^$', views.ProjectListView.as_view(), name='project-list'),
    url(r'^create/$', views.ProjectCreateView.as_view(), name='project-create'),
    url(r'^(?P<pk>\d+)/$', views.ProjectDetailView.as_view(), name='project-detail'),
    url(r'^(?P<pk>\d+)/update/$', views.ProjectUpdateView.as_view(), name='project-update'),
    url(r'^(?P<pk>\d+)/delete/$', views.ProjectDeleteView.as_view(), name='project-delete'),
]
