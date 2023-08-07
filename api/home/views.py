from django.contrib.auth.models import User, Group
from django.http import JsonResponse, Http404
from rest_framework import viewsets
from rest_framework import permissions, status
from home.serializers import UserSerializer, GroupSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Article
from .serializers import ArticleSerializer
import json
import os
import random


# TODO - make an API request to get the latest article

# TODO - make an API request to get the promoted article


@api_view(["GET"])
def main_page(request):
    info = {"this is the main page"}
    return Response(info)


"""
    return all the articles on the database
    url: get/articles
"""
@api_view(["GET"])
def get_articles(request):
    articles = Article.objects.all()
    serializer = ArticleSerializer(articles, many=True)
    print(articles)

    return Response({"data" : serializer.data})



"""
    This request returns a specify article by the id
    url: get/articles/{id}
"""
@api_view(["GET"])
def get_article(request, id):
    try:
        article = Article.objects.get(id=id)
        serializer = ArticleSerializer(article)

        return Response({"data": serializer.data})
        
    except Exception as e:
        return Response({"error" : f"{e}"})


"""
    this request creates a new article
    url: create/articles
"""
@api_view(["POST"])
def create_articles(request):
    try:
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message" : "article successfully created"})
        else:
            return Response({"message" : serializer.error_messages})
    except:
        return Response({"error": "something went wrong, please check the fields"})
    
   


"""
    delete articles based on the id
    url: delete/articles/{id}
"""
@api_view(["DELETE"])
def delete_articles(request, id):
    try:
        desired_article = Article.objects.get(id=id)

        desired_article.delete()
        return Response({"data": "article deleted successfully"})


    except Exception as e:
        return JsonResponse({"message": str(e)})
    

"""
    update articles based on the ID
    url: update/articles/{id}
"""
@api_view(["PUT"])
def update_articles(request, id):
    try:
        # Get the article that the user wants to update
        article_for_update = Article.objects.get(id=id)

        # Update the attributes of the retrieved article
        article_for_update.title = request.data["title"]
        article_for_update.description = request.data["description"]
        article_for_update.content = request.data["content"]
        article_for_update.author = request.data["author"]
        article_for_update.published = request.data["published"]

        # Save the updated article to the database
        article_for_update.save()

        return Response({"message": "article successfully updated"})
    except Exception as e:
        return Response({"data": f"{e}"})