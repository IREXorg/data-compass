from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('me/', views.ProfileView.as_view(), name='profile-detail'),
]
