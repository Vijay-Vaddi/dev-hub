from .models import Project, Tag
from django.db.models import Q
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator

def search_projects(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    
    # tags = Tag.objects.filter(name__icontains=search_query)
    # Q(tags__in=tags)
    # Q(owner__name__icontains=search_query)
    # can search by owner and then its child and what child contains
    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__name__icontains=search_query)
    )
    return projects, search_query

def paginate_projects(request, projects, per_page):
    page_num = request.GET.get('page')
    # page_obj = paginator.get_page(page_num)
    paginator = Paginator(projects, per_page=per_page)

    try:
        projects = paginator.page(page_num)
    # if page_num is not provided
    except PageNotAnInteger:
        page_num = 1
        projects = paginator.page(page_num)
    # if page_num is out of range
    except EmptyPage:
        page_num = paginator.num_pages
        projects = paginator.page(page_num)

    # to set custom range for pagination, set left/right index
    left_index = (int(page_num)-3)
    if left_index < 1:
        left_index = 1

    right_index = (int(page_num)+3)

    if right_index > paginator.num_pages:
        right_index = paginator.num_pages+1

    custom_range = range(left_index, right_index)

    return paginator, projects, custom_range 
