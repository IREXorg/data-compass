from django.urls import path

from . import views

app_name = 'surveys'

urlpatterns = [
    path('', views.SurveyListView.as_view(), name='survey-list'),
    path('create/', views.SurveyCreateView.as_view(), name='survey-create'),
    path('<int:pk>/', views.SurveyDetailView.as_view(), name='survey-detail'),
    path('<int:pk>/update/', views.SurveyUpdateView.as_view(), name='survey-update'),
    path('<int:pk>/delete/', views.SurveyDeleteView.as_view(), name='survey-delete'),
    path('<int:pk>/edit-start/', views.SurveyEditStartView.as_view(), name='survey-edit-start'),
    path('<int:pk>/edit-step-one/', views.SurveyEditStepOneView.as_view(), name='survey-edit-step-one'),
    path('<int:pk>/edit-step-two/', views.SurveyEditStepTwoView.as_view(), name='survey-edit-step-two'),
    path('<int:pk>/edit-step-three/', views.SurveyEditStepThreeView.as_view(), name='survey-edit-step-three'),
    path('<int:pk>/edit-step-four/', views.SurveyEditStepFourView.as_view(), name='survey-edit-step-four'),
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
    path(
        'dataset-response/<int:pk>/update-shared/',
        views.DatasetTopicSharedUpdateView.as_view(),
        name='dataset-response-update-shared'
    ),
    path(
        'dataset-response/<int:pk>/update-received/',
        views.DatasetTopicReceivedUpdateView.as_view(),
        name='dataset-response-update-received'
    ),
    path(
        '<int:pk>/response-resume/',
        views.SurveyResponseResumeView.as_view(),
        name='survey-response-resume'
    ),
    path(
        '<int:pk>/response-complete/',
        views.SurveyResponseCompleteView.as_view(),
        name='survey-response-complete'
    ),
    path(
        'responses/<int:pk>/',
        views.SurveyResponseDetailView.as_view(),
        name='survey-response-detail'
    ),
]
