from django.urls import path
from . import views


urlpatterns = [
    path("", views.main_page, name="home"),
    path("articles", views.get_articles, name="dontknow"),
    path("users", views.get_users, name="users"),
    path("create/articles", views.create_articles, name="createarticles")
]