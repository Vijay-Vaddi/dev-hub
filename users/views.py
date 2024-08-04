from django.shortcuts import render, redirect
from .models import Profile, User, Skill
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .form import CustomUserCreationForm, EditProfileForm, AddSkillForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .utils import search_profiles
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def profiles(request):
    profiles, search_query = search_profiles(request)
    per_page=2

    if request.GET.get('page'):
        page_num = request.GET.get('page')
    else: 
        page_num = 1

    paginator = Paginator(profiles, per_page=per_page)
    profiles = paginator.page(int(page_num))

    left_index = int(page_num)-3
    if left_index<1:
        left_index = 1

    right_index = int(page_num)+3
    if right_index>paginator.num_pages:
        right_index=paginator.num_pages

    custom_range = range(left_index, right_index)

    context = {'profiles':profiles, 'search_query':search_query, 
               'custom_range':custom_range }
    return render(request, 'users/profiles.html', context)


def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    # get skills with description by exlcuding
    top_skills = profile.skill_set.exclude(description__exact='')
    # get skills with no description
    other_skills = profile.skill_set.filter(description='')
    # get projets
    projects = profile.project_set.all()

    context = {'profile':profile, 'top_skills':top_skills, 
               "other_skills":other_skills, 'projects':projects }
    return render(request, 'users/user_profile.html', context)


def login_user(request):
    page = 'login'
    context = {'page': page}
    # if user is already logged in, redirect
    if request.user.is_authenticated:
         return redirect('profiles') 

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # check if user exists
        try:
            user = User.objects.get(username=username)    
        except:
            messages.error(request, 'Username does not exist')

        # check user by matching with password and login
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
                login(request, user)
                messages.info(request, 'Logged in')    
                return redirect('profiles')
        else:
            messages.error(request, 'username or password is incorrect')
    return render(request, 'users/login_register.html', context)


def register_user(request):
    page = 'register'
    form = CustomUserCreationForm()
    context = {'page':page, 'form':form}

    # register user 
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account created')
            login(request, user)
            return redirect('edit_account')
        
        messages.error(request, 'Registration failed for some reason')
        return render(request,'users/login_register.html', {'form':form, 'page':page})

    return render(request, 'users/login_register.html', context)


def logout_user(request):
     print(request)
     logout(request)
     messages.info(request, 'Logged out')
     return redirect('login')


# user account page
@login_required(login_url='login')
def user_account(request):
    # pass current user profile from request obj
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {'profile': profile, 'skills':skills, 'projects':projects}
    return render(request,'users/account.html', context)


@login_required(login_url='login')
def edit_account(request):
    # to edit logged in user, get user.profile from request
    profile = request.user.profile
    form = EditProfileForm(instance=profile)
    context = {'form': form}
    
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.username = profile.username.lower()
            profile.save()
            messages.success(request, 'Account edited')
            return redirect('user_account')
    
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def add_skill(request):
    form = AddSkillForm()
    profile = request.user.profile
    
    if request.method == 'POST':
        form = AddSkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill added')
            return redirect('user_account')
    context = {'form': form}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login')
def update_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    print(pk, skill)
    form = AddSkillForm(instance = skill)
    context = {'form': form}
    print('form  --- ',form)
    if request.method == 'POST':
        form = AddSkillForm(request.POST, instance = skill)
        print('form  --- ',form)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill updated')
            return redirect('user_account')

    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login')
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    print('inside delete skill view')
    if request.method == 'POST':
        skill.delete()
        print('deleted')
        # messages.success(request, 'Skill deleted')
        return redirect('user_account')
    context = {'object':skill}
    
    return render(request, 'projects/delete_object.html', context)
