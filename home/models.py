from django.db import models

from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # a foreinKey to user model, if user deleted, all post shuld be deleted
    body = models.TextField()
    slug = models.SlugField()
    # auto_now_add, complete the input automaticaly for FIRST time
    created = models.DateField(auto_now_add=True) #
    # auto_now update the Datetime field after every save
    updated = models.DateField(auto_now=True) # 


    def __str__(self):
        return f'{self.slug} - by: {self.user}'