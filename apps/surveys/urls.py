from django.urls import path

from . import views

app_name = 'surveys'

urlpatterns = [
    path('<int:pk>/consent', views.RespondentConsentView.as_view(), name='respondent-consent'),
    path('<int:pk>/respondent', views.RespondentUpdateView.as_view(), name='respondent-update'),
    path('<int:pk>/select-datasets', views.DatasetSelectView.as_view(), name='dataset-select'),
]
