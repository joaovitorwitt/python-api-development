from django.db import models
from pydantic import BaseModel
from typing import Optional


# Create your models here.


# model for the articles
# this will represent what the article will look like
class Article(BaseModel):
    id: int
    title : str
    description : str
    content : str
    category : list
    author : str
    # if the user does not provide anything it will evaluate to True (default)
    published: bool = True
    # create an optional
    rating: Optional[int] = None