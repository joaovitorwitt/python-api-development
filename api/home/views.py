from django.contrib.auth.models import User, Group
from django.http import JsonResponse, Http404
from rest_framework import viewsets
from rest_framework import permissions, status
from home.serializers import UserSerializer, GroupSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Article
import json
import os
import random


# TODO - make an APi request to get the latest article

# TODO - make an API request to get the promoted article


@api_view(["GET"])
def main_page(request):
    info = {"this is the main page"}
    return Response(info)

"""

"""
@api_view(["GET"])
def get_articles(request):
    directory = os.getcwd()
    filename = "articles.json"

    filepath = os.path.join(directory, filename)

    with open(filepath, "r") as file:
        articles_data = json.load(file)

    return Response({"data": articles_data})



"""
    This request returns a specify article by the id
    url: get/articles/{id}
"""
@api_view(["GET"])
def get_article(request, id):
    try:
        directory = os.getcwd()
        filename = "articles.json"
        filepath = os.path.join(directory, filename)

        with open(filepath, "r") as file:
            articles = json.load(file)

        for article in articles:
            if article["id"] == int(id):
                return Response({"article": f"here is the article: {article}"})
        
        raise Exception("Article not found")
    
    except Exception as e:
        return Response({"error" : f"{e}"})


"""
    this request creates a new article
    url: create/articles
"""
@api_view(["POST"])
def create_articles(request):
    try:
        article_data = Article.model_validate(request.data)
    except:
        return Response({"error": "something went wrong, please check the fields"})
    
    current_directory = os.getcwd()

    filename = "articles.json"
    filepath = os.path.join(current_directory, filename)

    if not os.path.exists(filepath):
        article_list = []
    else:
        with open(filepath, "r") as file:
            article_list = json.load(file)

    article_list.append(article_data.__dict__)

    with open(filepath, "w") as file:
        json.dump(article_list, file, indent=4)

    return Response({"message": "article successfully created", "article_data": article_data.model_dump()})


"""
    delete articles based on the id
    url: delete/articles/{id}
"""
@api_view(["DELETE"])
def delete_articles(request, id):
    try:
        current_directory = os.getcwd()
        filename = "articles.json"
        filepath = os.path.join(current_directory, filename)

        with open(filepath, "r") as file:
            articles = json.load(file)

        # creates a new list with the articles that do not have the id passed as parameter
        updated_articles = [article for article in articles if article["id"] != int(id)]

        if len(updated_articles) == len(articles):
            raise Exception("Article not found")

        # write the new file with the updated_articles
        with open(filepath, "w") as file:
            json.dump(updated_articles, file, indent=4)

        return JsonResponse({"message": "Article successfully deleted"})

    except Exception as e:
        return JsonResponse({"message": str(e)})
    

"""
    update articles based on the ID
    url: update/articles/{id}
"""
@api_view(["PUT"])
def update_articles(request, id):
    try:
        current_directory = os.getcwd()
        filename = "articles.json"
        filepath = os.path.join(current_directory, filename)

        with open(filepath, "r") as file:
            articles = json.load(file)

        # retrieved from the json file the article that will be updated
        desired_article = next((article for article in articles if article["id"] == int(id)), None)

        print(desired_article)

        # data that the user typed for the update
        article_data = Article.model_validate(request.data)

        desired_article["title"] = article_data.title
        desired_article["description"] = article_data.description
        desired_article["content"] = article_data.content
        desired_article["author"] = article_data.author
        desired_article["category"] = article_data.category
        desired_article["published"] = article_data.published

        print(desired_article)

        with open(filepath, "w") as file:
            json.dump(articles, file, indent=4)
    
        return Response({"message": "okay"})
    except:
        return Response({"message": "something went wrong"})