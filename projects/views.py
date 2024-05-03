from django.shortcuts import render
from django.http import HttpResponse
from .models import Project
from .forms import Create_project_form


def projects(request):
    projects = Project.objects.all()

    context = {'projects': projects}
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    
    project = Project.objects.get(id=pk)
    
    context = {'project':project}

    return render(request, 'projects/single_project.html', context)

def create_project(request):
    form = Create_project_form()
    context = {'form':form}
    return render(request, 'projects/project_form.html', context)
