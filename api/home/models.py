from django.db import models
from pydantic import BaseModel
from typing import Optional


# model for the articles
class Article(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField()
    author = models.CharField(max_length=100)
    published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
    

class UserModel(models.Model):
    email = models.CharField(max_length=255, unique=True)
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email