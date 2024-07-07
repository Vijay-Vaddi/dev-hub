from django.shortcuts import render
from .models import Profile
# Create your views here.

def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles':profiles}
    return render(request, 'users/profiles.html', context)

def user_profile(request, pk):
    # user_profile = Profile.objects.get(id=user.id)
    return render(request, 'users/user_profile.html')
