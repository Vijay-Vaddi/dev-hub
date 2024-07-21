from django.shortcuts import render, redirect
from .models import Profile, User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .form import CustomUserCreationForm
from django.contrib.auth.decorators import login_required

def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles':profiles}
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
            return redirect('profiles')
        
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