from django.urls import path

from . import views

app_name = 'surveys'

urlpatterns = [
    path('', views.SurveyListView.as_view(), name='survey-list'),
    path('<int:pk>/', views.SurveyDetailView.as_view(), name='survey-detail'),
    path('<int:pk>/update/', views.SurveyUpdateView.as_view(), name='survey-update'),
    path('<int:pk>/delete/', views.SurveyDeleteView.as_view(), name='survey-delete'),
    path('<int:pk>/unpublish/', views.SurveyUnpublishView.as_view(), name='survey-unpublish'),
    path('<int:pk>/publish/', views.SurveyPublishView.as_view(), name='survey-publish'),
    path('<int:pk>/share/', views.SurveyShareView.as_view(), name='survey-share'),
    path('<int:pk>/edit-start/', views.SurveyEditStartView.as_view(), name='survey-edit-start'),
    path('<int:pk>/edit-step-one/', views.SurveyEditStepOneView.as_view(), name='survey-edit-step-one'),
    path('<int:pk>/edit-step-two/', views.SurveyEditStepTwoView.as_view(), name='survey-edit-step-two'),
    path('<int:pk>/edit-step-three/', views.SurveyEditStepThreeView.as_view(), name='survey-edit-step-three'),
    path('<int:pk>/edit-step-four/', views.SurveyEditStepFourView.as_view(), name='survey-edit-step-four'),
    path('<int:pk>/edit-step-five/', views.SurveyEditStepFiveView.as_view(), name='survey-edit-step-five'),
    path('<int:pk>/edit-step-six/', views.SurveyEditStepSixView.as_view(), name='survey-edit-step-six'),
    path('<int:pk>/edit-finish/', views.SurveyEditFinishView.as_view(), name='survey-edit-finish'),

    # start: survey respondent paths
    path('<int:survey_pk>/create-respondent/', views.RespondentCreateView.as_view(), name='survey-create-respondent'),
    path('<int:pk>/delete-respondent/', views.RespondentDeleteView.as_view(), name='survey-delete-respondent'),
    path('<int:pk>/update-respondent/', views.RespondentUpdateView.as_view(), name='survey-update-respondent'),
    path(
        '<int:pk>/upload-respondents/',
        views.RespondentsUploadView.as_view(),
        name='survey-upload-respondents'
    ),
    # end: survey respondent paths

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

    # start: survey gender paths
    path('<int:survey_pk>/create-gender/', views.GenderCreateView.as_view(), name='survey-create-gender'),
    path('<int:survey_pk>/delete-gender/<int:pk>/', views.GenderDeleteView.as_view(), name='survey-delete-gender'),
    path('<int:pk>/update-gender/', views.GenderUpdateView.as_view(), name='survey-update-gender'),
    # end: survey gender paths

    # start: survey question paths
    path('<int:survey_pk>/create-question/', views.QuestionCreateView.as_view(), name='survey-create-question'),
    path('<int:pk>/delete-question/', views.QuestionDeleteView.as_view(), name='survey-delete-question'),
    path('<int:pk>/update-question/', views.QuestionUpdateView.as_view(), name='survey-update-question'),
    # end: survey question paths

    # start: survey logo paths
    path('<int:survey_pk>/create-logo/', views.LogoCreateView.as_view(), name='survey-create-logo'),
    path('<int:pk>/delete-logo/', views.LogoDeleteView.as_view(), name='survey-delete-logo'),
    path('<int:pk>/update-logo/', views.LogoUpdateView.as_view(), name='survey-update-logo'),
    # end: survey logo paths
]
