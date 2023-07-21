from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostUpdateForm


class HomeView(View):
    template_name = 'home/home.html'

    def get(self, request): # if user come with GET method
        posts = Post.objects.all()
        
        return render(request, 'home/home.html', {'posts':posts})
        

class PostDetailView(View):
    template_name = 'home/detail.html'
    def get(self, request, post_id, post_slug):
        post = Post.objects.get(pk=post_id, slug=post_slug)
        return render(request, self.template_name, {'post':post})
    


class PostDeleteView(LoginRequiredMixin ,View):
    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, 'Post deleted', 'success')
        else:
            messages.error(request, 'cant delete this post', 'warning')
        
        return redirect('account:user_profile', user_id=request.user.id)
    




class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostUpdateForm
    template_name = 'home/update.html'

    def dispatch(self, request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs['post_id'])
        print(post.user.id)
        print(request.user.id)

        if post.user.id != request.user.id:
            messages.error(request, 'you cant Edit this post', 'danger')
            return redirect('account:user_profile', user_id=request.user.id)
        # retruning super().dispatch() is very important
        # it used as else
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        form = self.form_class(instance=post)
        return render(request, self.template_name, {'form':form})
    
    def post(self, request, post_id):
        pass