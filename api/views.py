from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProjectSerializer
from projects.models import Project

# document like API to see all available endpoints
@api_view(['GET'])
def get_routes(request):
    routes = [
        {'GET':'/api/projects'},
        {'GET':'/api/projects/id'},
        {'POST':'/api/projects/id/vote'},

        {'POST':'/api/users/token'}, 
        {'POST':'/api/users/token/refresh'},
    ]
    
    return Response(routes)

@api_view(['GET'])
def get_projects(request):
    projects = Project.objects.all()
    # to serialize many objects set many=True, False for single obj
    serializer = ProjectSerializer(projects, many=True)
    
    return Response(serializer.data)


@api_view(['GET'])
def get_project(request, pk):
    project = Project.objects.get(id=pk)
    # to serialize many objects set many=True, False for single obj
    serializer = ProjectSerializer(project, many=False)
    
    return Response(serializer.data)