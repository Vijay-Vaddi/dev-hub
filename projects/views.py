from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm


def projects(request):
    projects = Project.objects.all()

    context = {'projects': projects}
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    
    project = Project.objects.get(id=pk)
    
    context = {'project':project}

    return render(request, 'projects/single_project.html', context)

def create_project(request):
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST) 
        if form.is_valid():
            form.save()
        return redirect('index')
        
    context = {'form':form}
    return render(request, 'projects/project_form.html', context)


def update_project(request, pk):
    
    proj = Project.objects.get(id=pk)

    # prefil form with proj obj to view in templates
    form = ProjectForm(instance=proj)

    if request.method == 'POST':
        # pass the second param instance=proj to let it know what proj to update
        form = ProjectForm(request.POST, instance=proj) 
        if form.is_valid():
            form.save()
        return redirect('index')
        
    context = {'form':form}
    return render(request, 'projects/project_form.html', context)



def delete_project(request):
    pass