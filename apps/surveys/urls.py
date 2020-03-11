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
    path('<int:pk>/edit-step-five/', views.SurveyEditStepFiveView.as_view(), name='survey-edit-step-five'),
    path('<int:pk>/edit-step-six/', views.SurveyEditStepSixView.as_view(), name='survey-edit-step-six'),
    path('<int:pk>/edit-finish/', views.SurveyEditFinishView.as_view(), name='survey-edit-finish'),
    path('<int:pk>/consent/', views.RespondentConsentView.as_view(), name='respondent-consent'),
    path('<int:pk>/respondent/update/', views.RespondentUpdateView.as_view(), name='respondent-update'),

    # start: survey role paths
    path('<int:survey_pk>/create-role/', views.RoleCreateView.as_view(), name='survey-create-role'),
    path('<int:pk>/delete-role/', views.RoleDeleteView.as_view(), name='survey-delete-role'),
    path('<int:pk>/update-role/', views.RoleUpdateView.as_view(), name='survey-update-role'),
    # end: survey role paths

    # start: survey topic paths
    path('<int:survey_pk>/create-topic/', views.TopicCreateView.as_view(), name='survey-create-topic'),
    path('<int:pk>/delete-topic/', views.TopicDeleteView.as_view(), name='survey-delete-topic'),
    path('<int:pk>/update-topic/', views.TopicUpdateView.as_view(), name='survey-update-topic'),
    # end: survey topic paths

    # start: survey dataset paths
    path('<int:survey_pk>/create-dataset/', views.DatasetCreateView.as_view(), name='survey-create-dataset'),
    path('<int:pk>/delete-dataset/', views.DatasetDeleteView.as_view(), name='survey-delete-dataset'),
    path('<int:pk>/update-dataset/', views.DatasetUpdateView.as_view(), name='survey-update-dataset'),
    # end: survey dataset paths

    # start: survey dataset-storage paths
    path(
        '<int:survey_pk>/create-dataset-storage/',
        views.DatasetStorageCreateView.as_view(),
        name='survey-create-dataset-storage'
    ),
    path(
        '<int:pk>/delete-dataset-storage/',
        views.DatasetStorageDeleteView.as_view(),
        name='survey-delete-dataset-storage'
    ),
    path(
        '<int:pk>/update-dataset-storage/',
        views.DatasetStorageUpdateView.as_view(),
        name='survey-update-dataset-storage'
    ),
    # end: survey dataset-storage paths

    # start: survey entity paths
    path('<int:survey_pk>/create-entity/', views.EntityCreateView.as_view(), name='survey-create-entity'),
    path('<int:pk>/delete-entity/', views.EntityDeleteView.as_view(), name='survey-delete-entity'),
    path('<int:pk>/update-entity/', views.EntityUpdateView.as_view(), name='survey-update-entity'),
    # end: survey entity paths

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
