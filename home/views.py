from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from .models import Post


class HomeView(View):
    template_name = 'hom/home.html'

    def get(self, request): # if user come with GET method
        posts = Post.objects.all()
        
        return render(request, 'home/home.html', {'posts':posts})
        

class PostDetailView(View):
    template_name = 'home/detail.html'
    def get(self, request, post_id, post_slug):
        post = Post.objects.get(pk=post_id, slug=post_slug)
        return render(request, self.template_name, {'post':post})