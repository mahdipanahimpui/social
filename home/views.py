from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostCreateUpdateForm
from django.utils.text import slugify


class HomeView(View):
    template_name = 'home/home.html'

    def get(self, request): # if user come with GET method
        posts = Post.objects.all()
        # posts = Post.objects.order_by('-created') # ordered just here but, you can use Meta class in models.py
        
        return render(request, 'home/home.html', {'posts':posts})
        

class PostDetailView(View):
    template_name = 'home/detail.html'
    def get(self, request, post_id, post_slug):
        # post = Post.objects.get(pk=post_id, slug=post_slug)
        post = get_object_or_404(Post, pk=post_id, slug=post_slug)
        comments = post.post_comments.filter(is_reply=False)
        return render(request, self.template_name, {'post':post, 'comments': comments})
    


class PostDeleteView(LoginRequiredMixin ,View):
    def get(self, request, post_id):
        # post = Post.objects.get(pk=post_id)
        post = get_object_or_404(Post, pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, 'Post deleted', 'success')
        else:
            messages.error(request, 'cant delete this post', 'warning')
        
        return redirect('account:user_profile', user_id=request.user.id)
    




class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm
    template_name = 'home/update.html'

    # setup handle fields that is shared in methods
    # why we dont use Class Variable? => class variable run after define
    # the below setup method optimize the connection to database, (Once)
    # setup run befor dispatch
    def setup(self, request, *args, **kwargs):
        # self.post_instance = Post.objects.get(pk=kwargs['post_id'])
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().setup(self, request, *args, **kwargs)

    # dispatch runs befor all methods after that, and prevent repeating codes
    def dispatch(self, request, *args, **kwargs):
        # post = Post.objects.get(pk=kwargs['post_id'])  # setup handles
        post = self.post_instance
        print(post.user.id)
        print(request.user.id)

        if post.user.id != request.user.id:
            messages.error(request, 'you cant Edit this post', 'danger')
            return redirect('account:user_profile', user_id=request.user.id)
        # retruning super().dispatch() is very important
        # it used as else
        return super().dispatch(request, *args, **kwargs)

    # insted post_id param use *args, **kwargs
    def get(self, request, *args, **kwargs):
        # post = Post.objects.get(pk=post_id) # setup handles
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, self.template_name, {'form':form})
    
    # insted post_id param use *args, **kwargs
    def post(self, request, *args, **kwargs):
        # post = Post.objects.get(pk=post_id) # setup handles
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)

        if form.is_valid():
            new_post = form.save(commit=False) # save the new post, but not connect to database
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request, 'post updated', 'success')
            return redirect('home:post_detail', post.id, post.slug)
        

class PostCreateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm
    template_name = 'home/create.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        new_post = form.save(commit=False)
        new_post.user = request.user
        new_post.slug = slugify(form.cleaned_data['body'][:30])
        new_post.save()
        messages.success(request, 'Post Created', 'success')
        return redirect('home:post_detail', new_post.id, new_post.slug) 


