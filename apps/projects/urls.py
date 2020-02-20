from django.urls import path

from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path('store', views.store, name='store'),
    path('show/<project_id>', views.show, name='show'),
]
