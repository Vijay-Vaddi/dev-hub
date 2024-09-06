from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import ProjectSerializer
from projects.models import Project, Review, Tag

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
# @permission_classes([IsAuthenticated])
def get_projects(request):
    print("USER", request.user)
    projects = Project.objects.all()
    # to serialize many objects set many=True, False for single obj
    serializer = ProjectSerializer(projects, many=True)
    
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_project(request, pk):
    project = Project.objects.get(id=pk)
    # to serialize many objects set many=True, False for single obj
    serializer = ProjectSerializer(project, many=False)
    
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def project_vote(request, pk):
    project = Project.objects.get(id=pk)
    # coming from token auth, not session
    user = request.user.profile
    # .data is available due to @api_view making it rest
    data = request.data

    review, created = Review.objects.get_or_create(
        owner=user,
        project=project, 
    )

    review.value = data['value']
    review.save()
    project.get_vote_count

    serializer = ProjectSerializer(project, many=False)

    return Response(serializer.data)


@api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
def delete_tags(request):
    print(request.user)

    project = Project.objects.get(id=request.data['project_id'])
    tag = project.tags.get(id=request.data['tag_id'])

    # profile = request.user.profile
    # proj_id = request.data['proj_id']
    # tag_id = request.data['tag_id']

    # proj = profile.project_set.get(id=proj_id)
    # tag = proj.tags.get(id=tag_id)
    project.tags.remove(tag)
    # tag.delete() 

    return Response({'Tag was deleted'})