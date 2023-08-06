from django.urls import path
from . import views


urlpatterns = [
    path("", views.main_page, name="home"),
    path("get/articles", views.get_articles, name="getarticles"),
    path("get/articles/<int:id>", views.get_article, name="getarticle"),
    path("create/articles", views.create_articles, name="createarticles"),
    path("delete/articles/<int:id>", views.delete_articles, name="deletearticles")
]