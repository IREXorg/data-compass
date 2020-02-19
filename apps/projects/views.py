from django.shortcuts import render

from apps.projects.models import Project

def index(request):
    context = {}

    return render(request, 'projects/index.html', context)
