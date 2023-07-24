from django.db import models

from django.contrib.auth.models import User
from django.urls import reverse


"""
    models should be thick and views should be thin
"""


class Post(models.Model):
    ########## for backward relations #########
    # u is a User instance
    # u.Post.all() => ERROR (Note!!: in O2O relation is ok)
    # solution: add <_set> u.Post_set.all() for M2M & M2O relations
    # other way: add <related_name> for field, so => u.<related_name> is OK
    # ** Does not need migration ** for adding related_name
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts') # a foreinKey to user model, if user deleted, all post shuld be deleted
    body = models.TextField()
    slug = models.SlugField()
    # auto_now_add, complete the input automaticaly for FIRST time
    created = models.DateField(auto_now_add=True) #
    # auto_now update the Datetime field after every save
    updated = models.DateField(auto_now=True) # 


    def __str__(self):
        return f'{self.slug} - by: {self.user}'
    
    # ordered in all queries
    class Meta:
        ordering = ('-created', '-updated', 'body')
    

    def get_absolute_url(self):
        return reverse('home:post_detail', args=[self.id, self.slug])
    
    def likes_count(self):
        return self.plikes.count()
    

    def user_can_like(self, user):
        user_like = user.ulikes.filter(post=self)
        if user_like.exists():
            return False
        return True

    




class Comment(models.Model):

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_comments')
    # if Post class is created bellow of Comment class use 'Post' insted Post  (in ForeigKey)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    body = models.TextField(max_length=400)
    # insted 'self' you can use 'Comment'
    # blank and null allows to make reply null, null=True is on DATABASE, blank=True is Django level and for validation
    reply = models.ForeignKey('self', on_delete=models.CASCADE ,related_name='rcomments', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.user} C/R TO {self.body}'
    


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ulikes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="plikes")
    

    def __str__(self):
        return f'{self.user} liked {self.post.slug}'
    



