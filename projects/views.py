from django.shortcuts import render, redirect
from .models import Project
from .forms import ProjectForm

# view for all projects list
def projects(request):
    projects = Project.objects.all()
    context = {'projects': projects}

    return render(request, 'projects/projects.html', context)

# view for single project item
def project(request, pk): 
    project = Project.objects.get(id=pk)
    context = {'project':project}

    return render(request, 'projects/single_project.html', context)

# create project item view
def create_project(request):
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
        return redirect('index')
        
    context = {'form':form}
    return render(request, 'projects/project_form.html', context)

# update project item
def update_project(request, pk):    
    proj = Project.objects.get(id=pk)

    # prefil form with proj obj to view in templates
    form = ProjectForm(instance=proj)

    if request.method == 'POST':
        # pass the second param instance=proj to let it know what proj to update
        form = ProjectForm(request.POST, request.FILES, instance=proj) 
        if form.is_valid():
            form.save()
        return redirect('index')
        
    context = {'form':form}
    return render(request, 'projects/project_form.html', context)

# delete project
def delete_project(request, pk):
    proj = Project.objects.get(id=pk)
    context = {'object':proj}
    
    if request.method=='POST':
        proj.delete()
        return redirect('index')
    
    return render(request, 'projects/delete_object.html', context)