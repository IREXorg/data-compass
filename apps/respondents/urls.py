from django.urls import path

from . import views

app_name = 'respondents'

urlpatterns = [
    path('', views.RespondentListView.as_view(), name='respondent-list'),
    path('invite/', views.RespondentInviteView.as_view(), name='respondent-invite'),
    path('<int:pk>/update/', views.RespondentUpdateView.as_view(), name='respondent-update'),
    path('<int:survey>/consent/', views.RespondentConsentView.as_view(), name='respondent-consent'),
]
