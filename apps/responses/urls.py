from django.urls import path

from . import views

app_name = 'responses'

urlpatterns = [
    # response
    path(
        '',
        views.SurveyResponseListView.as_view(),
        name='survey-response-list'
    ),
    path(
        '<int:pk>/',
        views.SurveyResponseDetailView.as_view(),
        name='survey-response-detail'
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

    # dataset response
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

    # dataset-topic-response
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

    # exports
    path(
        '<int:survey>/datasets-shared',
        views.DatasetSharedListView.as_view(),
        name='dataset-shared-list'
    ),
    path(
        '<int:survey>/datasets-received',
        views.DatasetReceivedListView.as_view(),
        name='dataset-received-list'
    ),
    path(
        '<int:survey>/datasets-storage',
        views.DatasetStorageAccessListView.as_view(),
        name='dataset-storage-access-list'
    ),
    path(
        '<int:survey>/dataset-responses',
        views.DatasetResponseListView.as_view(),
        name='dataset-response-list'
    ),
]
