from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework import permissions, status
from home.serializers import UserSerializer, GroupSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Article
import json
import os

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
    directory = os.getcwd()
    filename = "articles.json"

    filepath = os.path.join(directory, filename)

    with open(filepath, "r") as file:
        articles_data = json.load(file)

    return Response({"data": articles_data})



@api_view(["POST"])
def create_articles(request):
    try:
        article_data = Article.model_validate(request.data)
    except:
        return Response({"error": "something went wrong, please check the fields"})
    
    # Get the current working directory
    current_directory = os.getcwd()

    filename = "articles.json"
    filepath = os.path.join(current_directory, filename)

    # Check if the file exists, and if not, create an empty list to hold the articles
    if not os.path.exists(filepath):
        article_list = []
    else:
        # If the file exists, load the existing articles from the file
        with open(filepath, "r") as file:
            article_list = json.load(file)

    # Append the new article_data to the list of articles
    article_list.append(article_data.__dict__)

    # Save the updated list of articles to the JSON file
    with open(filepath, "w") as file:
        json.dump(article_list, file, indent=4)

    return Response({"message": "article successfully created", "article_data": article_data.model_dump()})



@api_view(["GET"])
def get_users(request):
    users = ["John Doe", "Mary Smith"]
    return Response(users)

