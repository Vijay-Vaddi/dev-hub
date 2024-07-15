from django.shortcuts import render, redirect
from .models import Profile, User
from django.contrib.auth import login, authenticate
# Create your views here.

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

def login_page(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # check if user exists
        try:
            user = User.objects.get(username=username)    
            print('obj', user)
        except:
            print('Username or does not exist')

        # check user by matching with password and login
        user = authenticate(request, username=username, password=password)
        print('authen', user)
        
        if user is not None:
                login(request, user)    
                return redirect('profiles')
        else:
            print('username or password is incorrect')
    return render(request, 'users/login.html')