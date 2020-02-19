from django.shortcuts import render

from apps.projects.models import Project

def index(request):
    p = Project(name='Foo Name', description='This is a description')
    projects = [p,[]]

    context = { 'projects': projects }

    return render(request, 'projects/index.html', context)
