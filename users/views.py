from django.shortcuts import render
from .models import Profile
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
    return render(request, 'users/login.html')