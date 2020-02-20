from django.shortcuts import redirect, render

from apps.projects.models import Project

def index(request):
    all_projects = Project.objects.all()
    total_surveys = len([])

    context = { 'projects': all_projects, 'total_surveys': total_surveys }
    return render(request, 'projects/index.html', context)

def create(request):
    context={}

    return render(request, 'projects/create.html', context)

def store(request):
    project_name = request.POST.get('project_name')
    project_description = request.POST.get('project_description')

    Project.objects.create(name=project_name, description=project_description, creator_id=1)

    return redirect('projects:index')

def show(request, project_id):
    project = Project.objects.filter(pk=project_id)

    context = { 'project': project }
    return render(request, 'projects/show.html', context)

