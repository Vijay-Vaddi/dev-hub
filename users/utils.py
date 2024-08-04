from django.db.models import Q
from .models import Profile, Skill
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

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
    # return profiles_pagination(request, profiles, 2), search_query

def profiles_pagination(request, profiles, per_page):
    
    if request.GET.get('page'):
        page_num = request.GET.get('page')
    else: 
        page_num = 1

    paginator = Paginator(profiles, per_page=per_page)
    try:
        profiles = paginator.page(int(page_num))
    except PageNotAnInteger:
        page_num=1
        profiles = paginator.page(int(page_num))
    except EmptyPage:
        page_num = paginator.num_pages
        profiles = paginator.page(page_num)

    left_index = int(page_num)-3
    if left_index<1:
        left_index = 1

    right_index = int(page_num)+3

    if right_index>paginator.num_pages:
        right_index=paginator.num_pages+1

    custom_range = range(left_index, right_index)

    return profiles, custom_range


