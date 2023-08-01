from django.urls import path
from .views import CreatePostsView, GetPostsView


urlspatters = [
    path("posts/", GetPostsView.as_view(), name="get-posts")
]