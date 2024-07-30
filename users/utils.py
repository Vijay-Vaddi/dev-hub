from django.db.models import Q
from .models import Profile, Skill

def search_profiles(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')  
        print(search_query)
    # to search by skills get the exact skills in while list first
    skills = Skill.objects.filter(name__icontains=search_query)

    # profiles = Profile.objects.all()
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) | 
        Q(short_intro__icontains=search_query) |
        Q(skill__in=skills)) #can search in child object this way, this will create ducplicates, so add distict

    return profiles, search_query