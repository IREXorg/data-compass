from django.urls import path

from . import views

app_name = 'surveys'

urlpatterns = [
    path('', views.SurveyListView.as_view(), name='survey-list'),
    path('create/', views.SurveyCreateView.as_view(), name='survey-create'),
    path('<int:pk>/', views.SurveyDetailView.as_view(), name='survey-detail'),
    path('<int:pk>/update/', views.SurveyUpdateView.as_view(), name='survey-update'),
    path('<int:pk>/delete/', views.SurveyDeleteView.as_view(), name='survey-delete'),
    path('<int:pk>/consent/', views.RespondentConsentView.as_view(), name='respondent-consent'),
    path('<int:pk>/respondent/update/', views.RespondentUpdateView.as_view(), name='respondent-update'),
    path(
        '<int:pk>/select-datasets/',
        views.DatasetResponseListCreateView.as_view(),
        name='dataset-response-list-create'
    ),
    path(
        'dataset-response/<int:pk>/update-frequency/',
        views.DatasetResponseUpdateFrequencyView.as_view(),
        name='dataset-response-update-frequency'
    ),
    path(
        'dataset-topic-response/<int:pk>/update/',
        views.DatasetTopicResponseUpdateView.as_view(),
        name='dataset-topic-response-update'
    ),
]
