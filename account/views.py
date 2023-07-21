from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'account/register.html'

    # dispatch method runs befor all methods in class
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        # return super is required if code is continued
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form}) # account dir is template/account
    
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password'])
            messages.success(request, 'User Registered', 'success')
            return redirect('home:home')
        
        return render(request, self.template_name, {'form':form})
    

class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'account/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        # return super is required if code is continued
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, auth_field=cd['auth_field'], password=cd['password'])


            if user is not None:
                login(request, user)
                messages.success(request, 'user logged in', 'success')
                return redirect('home:home')
        
            messages.error(request, 'username or password is wrong', 'warning')

        return render(request, self.template_name, {'form':form})

            
class UserLogoutView(LoginRequiredMixin ,View):
    # for LoginRequiredMixin add
    # login_url = '/account/login'
    # if user is not login redirect to login page
    # other way is adding LOGING_URL = '/account/login' to setting.py

    def get(self, request):
        logout(request)
        messages.success(request, 'user logout', 'success')
        return redirect('home:home')
    


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, user_id): # user_id name must be same name as in path arg
        user = User.objects.get(pk=user_id)
        # filter VS get
        # 1 filter need for loop
        # filter retrun many item
        # if get cant found raise error

        # for foreinKey we need Instance(user), id or pk not working here
        posts = Post.objects.filter(user=user)
        return render(request, 'account/profile.html', {'user':user, 'posts': posts})