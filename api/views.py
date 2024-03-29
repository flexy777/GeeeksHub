from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import ProjectSerializer, ProfileSerializer
from projects.models import Project, Review, Tag
from users.models import Profile

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET' : 'api/projects'},
        {'GET' : 'api/users'},
        {'GET' : 'api/projects/id'},
        {'POST' : 'api/projects/id/vote'},

        {'POST' : 'api/users/token'},
        {'POST' : 'api/users/token/refresh'}


    ]
    return Response(routes)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getProjects(request):
    # print('USER:', request.user)
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getProject(request, pk):
    project = Project.objects.get(id=pk)
    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)

@api_view(['POST', 'PUT'])
@permission_classes([IsAuthenticated])
def projectVote(request, pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile        # the request(user) is from the access token not from the request because we are dealing with api
    data = request.data
    review, created = Review.objects.get_or_create(
        owner = user,
        project = project,

    )
    review.value = data['value']
    review.save()
    project.getVoteCount
    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
def removeTag(request):
    tagId = request.data['tag']
    projectId = request.data['project']

    project = Project.objects.get(id=projectId)
    tag = Tag.objects.get(id=tagId)

    project.tags.remove(tag)
    return Response('Tag was deleted')

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getUsers(request):
    # print('USER:', request.user)
    user = Profile.objects.all()
    serializer = ProfileSerializer(user, many=True)
    return Response(serializer.data)