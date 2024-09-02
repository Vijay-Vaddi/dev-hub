from django.shortcuts import render, redirect
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required 
from django.db.models import Q
from .utils import search_projects, paginate_projects
from django.contrib import messages
from django.db import IntegrityError

# view for all projects list
def projects(request):
    
    projects, search_query = search_projects(request)
    paginator, projects, custom_range = paginate_projects(request, projects, per_page=3)

    context = {'projects': projects, 'search_query': search_query,
                'paginator':paginator,  'custom_range':custom_range }

    return render(request, 'projects/projects.html', context)

# view for single project item
def project(request, pk): 
    project = Project.objects.get(id=pk)
    form = ReviewForm()
    print(form.fields['value'].label)
    print(form.fields['body'].label)
    try:
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            review = form.save(commit=False)
            review.project = project
            review.owner = request.user.profile
            review.save()
            
            # update vote count, this will run the get_vote_count and update it
            project.get_vote_count

            messages.success(request, 'Review submitted')
            return redirect('project', pk=project.id)
    except IntegrityError:
        messages.error(request, 'Can not submit review again')
    
    print(project.reviewers)

    context = {'project':project, 'form':form}

    return render(request, 'projects/single_project.html', context)

# create project item view
@login_required(login_url='login')
def create_project(request):
    # get owner of the project from profile 
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        new_tags = request.POST.get('new_tags').replace(',', ' ').title().split()

        form = ProjectForm(request.POST, request.FILES) 
        if form.is_valid():
            project = form.save(commit=False)
            # add owner to project and then save
            project.owner = profile
            project.save()
            
            # add tags to project
            for tag in new_tags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)

        return redirect('user_account')
        
    context = {'form':form}
    return render(request, 'projects/project_form.html', context)

# update project item
@login_required(login_url='login')
def update_project(request, pk):    
    # get logged in user
    profile = request.user.profile
    '''proj = Project.objects.get(id=pk) 
    # this will make any logged in user edit with pk, so XX
    '''
    # query only in logged in users project_set
    proj = profile.project_set.get(id=pk)

    # prefil form with proj obj to view in templates
    form = ProjectForm(instance=proj)

    if request.method == 'POST':
        new_tags = request.POST.get('new_tags').replace(',', ' ').title().split()
        
        # pass the second param instance=proj to let it know what proj to update
        form = ProjectForm(request.POST, request.FILES, instance=proj) 
        if form.is_valid():
            project = form.save()

            for tag in new_tags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)

        return redirect('user_account')
        
    context = {'form':form}
    return render(request, 'projects/project_form.html', context)

# delete project
@login_required(login_url='login')
def delete_project(request, pk):
    # check projects in logged in users proj set only
    profile = request.user.profile
    proj = profile.project_set.get(id=pk)
    context = {'object':proj}
    
    if request.method=='POST':
        proj.delete()
        return redirect('user_account')
    
    return render(request, 'projects/delete_object.html', context)
