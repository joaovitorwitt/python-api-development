from django.contrib.auth.models import User , Group
from django.http import JsonResponse, Http404
from rest_framework import viewsets
from rest_framework import permissions, status
from home.serializers import UserSerializer, GroupSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import Article, UserModel
from .serializers import ArticleSerializer, UserSerializer
import json
import os
import random
from .utils import hash_password, create_access_token, compare_hashed_passwords
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, SessionAuthentication

# TODO - make an API request to get the latest article

# TODO - make an API request to get the promoted article


@api_view(["GET"])
def main_page(request):
    info = {"this is the main page"}
    return Response(info)


######################################################################
# API endpoints for dealing with authetication (/login, /register)
######################################################################

"""
    User Registration Endpoint
    --------------------------

    This endpoint allows users to register and create a new account.

    URL: /register
    Method: POST

    Parameters (POST data):
    - username (string, required): The desired username for the new user.
    - email (string, required): The email address of the new user.
    - password (string, required): The password for the new account.

    Responses:
    - 201 Created: User registration successful.
        {
            "message": "User successfully registered",
            "token": "<JWT_TOKEN>"
        }
    - 400 Bad Request: Invalid input or missing required fields.
        {
            "serializer error": {
                "field_name": ["error_message"]
            }
        }
    - 500 Internal Server Error: An error occurred during registration.
        {
            "error message": "Internal server error details"
        }

    Notes:
    - The password provided will be securely hashed before being stored.
    - Upon successful registration, a JSON Web Token (JWT) will be returned in the response.
      This token can be used for subsequent authentication and authorization.
    - In case of an invalid request, the response will provide details about the validation errors.
    - If an error occurs during registration, the response will contain an error message.

    Example Usage:
    --------------
    ```
    POST /register
    {
        "username": "new_user",
        "email": "new_user@example.com",
        "password": "secretpassword"
    }
    ```
"""
@api_view(['POST'])
def register_user(request):
    try:
        serializer = UserSerializer(data=request.data)

        email = request.data['email']

        # Check if a user with the given email already exists
        if User.objects.filter(email=email).exists():
            return Response({"message": "An account with this email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            hashed_password = hash_password(serializer.validated_data['password'])
            serializer.validated_data["password"] = hashed_password
            user = serializer.save()
            token = create_access_token(user)
            return Response({"message": "user successfully registered", "token" : token.key})
        else:
            return Response({"serializer error" : serializer.errors})
    except Exception as e:
        return Response({"error message": f"{e}"})


"""
    endpoint for logging the user
    url: /login
"""
@api_view(['POST'])
@authentication_classes([BasicAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def login(request):
    try:
        username = request.data["username"]
        user = User.objects.get(username=username)   
        user_serializer = UserSerializer(user).data     
        return Response({"message": user_serializer})
    except Exception as e:
        return Response({"error" : f"{e}"})


#######################################################
# API endpoints for dealing with articles
#######################################################
# TODO - validate email
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
    

#######################################################
# API endpoints for dealing with user
#######################################################
"""
    list all the users on the database
    url: get/users
"""
@api_view(['GET'])
def list_users(request):
    try:
        users = UserModel.objects.all()
        users_serializers = UserSerializer(users, many=True).data

        return Response({"users": users_serializers})

    except Exception as e:
        return Response({"message": f"{e}"})
    

"""
    return users by the id
    url: get/users/{id}
"""
@api_view(['GET'])
def return_user(request, id):
    try:
        user = UserModel.objects.get(id=id)
        serialize_user = UserSerializer(user).data
        return Response({"user": serialize_user})
    
    except Exception as e:
        return Response({"message": f"{e}"})


"""
    create a new user
    url: create/user
"""
@api_view(['POST'])
def create_user(request):
    try:

        hashed_password = hash_password(request.data["password"])
        user_data = request.data.copy()
        user_data["password"] = hashed_password
        user_serializer = UserSerializer(data=user_data)

        if user_serializer.is_valid():
            user = user_serializer.save()
            token = create_access_token(user)
            return Response({"message": f"user created successfully", "token" : token.key})
        else:
            return Response({"error": user_serializer.errors})
    except Exception as e:
        return Response({"message": f"{e}"})


"""
    delete some user based on the id
    url: delete/user/{id}
"""
@api_view(['DELETE'])
def delete_user(request, id):
    try:
        desired_user = UserModel.objects.get(id=id)
        desired_user.delete()

        return Response({"message": "user deleted successfully"})

    except Exception as e:
        return Response({"error": f"{e}"})
    

"""
    update the user based on its id
    url: update/user/{id}
"""

@api_view(['PUT'])
def update_user(request, id):
    try:
        # retrieve user from db
        user_for_update = UserModel.objects.get(id=id)

        user_for_update.email = request.data["email"]
        user_for_update.password = request.data["password"]
        
        user_for_update.save()

        return Response({"message": "user updated successfully"})

    except Exception as e:
        return Response({"message": f"{e}"})