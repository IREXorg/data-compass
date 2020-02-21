from django.conf.urls import url

from . import views

app_name = 'surveys'

urlpatterns = [
    url(r'^$', views.SurveyListView.as_view(), name='survey-list'),
    url(r'^create/$', views.SurveyCreateView.as_view(), name='survey-create'),
    url(r'^(?P<pk>\d+)/$', views.SurveyDetailView.as_view(), name='survey-detail'),
    url(r'^(?P<pk>\d+)/update/$', views.SurveyUpdateView.as_view(), name='survey-update'),
    url(r'^(?P<pk>\d+)/delete/$', views.SurveyDeleteView.as_view(), name='survey-delete'),
]
