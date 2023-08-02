from django.db import models
from pydantic import BaseModel



# Create your models here.


# model for the articles
# this will represent what the article will look like
class Article(BaseModel):
    title : str
    description : str
    content : str
    category : list
    # if the user does not provide anything it will evaluate to True (default)
    published: bool = True
    # create an optional