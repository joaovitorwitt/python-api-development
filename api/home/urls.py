from django.urls import path
from . import views


urlpatterns = [
    path("", views.main_page, name="home"),
    path("get/articles", views.get_articles, name="getarticles"),
    path("get/articles/<int:id>", views.get_article, name="getarticle"),
    path("create/articles", views.create_articles, name="createarticles"),
    path("delete/articles/<int:id>", views.delete_articles, name="deletearticles"),
    path("update/articles/<int:id>", views.update_articles, name="updatearticle"),
    path("get/users", views.list_users, name="listusers"),
    path("get/users/<int:id>", views.return_user, name="returnuser"),
    path("create/user", views.create_user, name="createuser"),
    path("delete/user/<int:id>", views.delete_user, name="deleteuser"),
    path("update/user/<int:id>", views.update_user, name="updateuser"),
    path("login", views.login, name="login"),
    path("register", views.register_user, name="register")
]

# TODO - create /login route (username + password) ===> if credentials are valid ==> create JWT token