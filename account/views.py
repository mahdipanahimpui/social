from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


class UserRegisterView(View):
    form_class = UserRegisterForm
    template_name = 'account/register.html'

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

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])

            print(user)

            if user is not None:
                login(request, user)
                messages.success(request, 'user logged in', 'success')
                return redirect('home:home')
        
            messages.error(request, 'username or password is wrong', 'warning')

        return render(request, self.template_name, {'form':form})

            
class UserLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'user logout', 'success')
        return redirect('home:home')