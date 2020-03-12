from django.urls import path

from . import views

app_name = 'responses'

urlpatterns = [
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
        'responses/',
        views.SurveyResponseListView.as_view(),
        name='survey-response-list'
    ),
    path(
        'responses/<int:pk>/',
        views.SurveyResponseDetailView.as_view(),
        name='survey-response-detail'
    ),
]
