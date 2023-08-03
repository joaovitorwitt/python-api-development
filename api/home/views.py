from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions, status
from home.serializers import UserSerializer, GroupSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Article



##################################
"""
    API basic CRUD operations
"""

@api_view(['GET'])
def get(request):
    return Response("information retrieved")


@api_view(['DELETE'])
def delete(request):
    return Response("Information deleted")


@api_view(['POST'])
def create(request):
    information = request.data
    return Response(f"information created: {information}")


@api_view(['PUT'])
def update(request):
    information = request.data
    return Response(f"information updated: {information}")

"""
    End of API CRUD operations
"""
#######################################


@api_view(["GET"])
def main_page(request):
    info = {"this is the main page"}
    return Response(info)


@api_view(["GET"])
def get_articles(request):
    data = [
        {
            "title": "O que houve com Sr Miles?",
            "description": "CONTO, Evento Inicial",
            "content" : "lorem ipsum....."
        },
        {
            "title": "Violeta Waldemir",
            "description": "another random description",
            "content" : "lorem ipsudasdasdasd sda sd"
        },
        {
            "title": "Eles encontraram o corpo?",
            "description": "o que se sabe",
            "content" : "lorem ipsum.....dasdasdadasdads"
        },
            
    ]
    return Response(data)


@api_view(["POST"])
def create_articles(request):
    try:
        article_data = Article.model_validate(request.data)
    except:
        return Response({"error": "something went wrong, please check the fields"})
    print(article_data)

    return Response({f"article successfully created" : article_data.model_dump()})




@api_view(["GET"])
def get_users(request):
    users = ["John Doe", "Mary Smith"]
    return Response(users)

