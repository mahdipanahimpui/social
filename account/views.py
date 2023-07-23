from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post
from account.models import Relation
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy



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
    # by adding next after loging, user redirect to last page that wants to see
    form_class = UserLoginForm
    template_name = 'account/login.html'

    def setup(self, request, *args, **kwargs):
        # GET is a sending method in web
        # get is a method in python, second arg is optional, .get('next', None)
        # get returns None by default
        self.next = request.GET.get('next' )
        return super().setup(request, *args, **kwargs)


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
                if self.next:
                    return redirect(self.next)
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
        # user = User.objects.get(pk=user_id)
        user = get_object_or_404(User, pk=user_id)
        # filter VS get
        # 1 filter need for loop
        # filter retrun many item
        # if get cant found raise error

        # for foreinKey we need Instance(user), id or pk not working here
        # filter return an empty list if not found anything, but could handled by **get_list_or_404** 

        # posts = Post.objects.filter(user=user) # insted this code, use related_name
        posts = user.user_posts.all()

        is_following = False
        relation = Relation.objects.filter(from_user=request.user, to_user=user).exists()
        if relation:
            is_following = True

        return render(request, 'account/profile.html', {'user':user, 'posts': posts, 'is_following': is_following})
    




# sending email 
# user send email in input field in template_name(password_reset_form.html)
# an email as email_template_name shape(account/password_reset_email.html) is sent to user by app
# after sending email to user, success_url('account:password_reset_home') is shown
class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done') # because it is class variable, it try to access url, 
    # *** but url does not exists yet sor use reverse_lazey ***
    # success_url = reverse_lazy('account:password_reset_home')
    email_template_name = 'account/password_reset_email.html'


## after sending email to user, success_url('account:password_reset_home') is shown by calling below
# view by UserPasswordResetView
class UserPasswordResetDoneView(auth_views.PasswordChangeDoneView):
    template_name = 'account/password_reset_done.html'


## showing a page that access to user to change him/his passowrd and confirm it
# this view need uidb64 and token
# the url of this view is shown in email context in password_reset_email.html
class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    # an template that use to change password
    template_name = 'account/password_reset_confirm.html'
    success_url =  reverse_lazy('account:password_reset_complete')


class UserPasswordResetComplete(auth_views.PasswordResetCompleteView):
    template_name =  'account/password_reset_complete.html'



class FollowingInit:
    def __init__(self, request, *args, **kwargs):
        self.to_user_id = kwargs['to_user_id']
        self.to_user = User.objects.get(pk=self.to_user_id)
        self.relation = Relation.objects.filter(from_user=request.user, to_user=self.to_user)

        if self.to_user == request.user:
            messages.error(request, 'you cant follow yourself')
            return redirect('account:user_profile', user_id=self.to_user_id)
        



class UserFollowView(LoginRequiredMixin, View):

    def get(self, request, to_user_id):
        
        following_init = FollowingInit(request, to_user_id=to_user_id)
        relation = following_init.relation
        to_user = following_init.to_user

        if relation.exists():
            messages.error(request, 'you`ve been Followed already', 'warning')
        else:
            # Relation.objects.create(from_user=request.user, to_user=user) it SVAE automatically , or in the below way(needs SAVE)
            Relation(from_user=request.user, to_user=to_user).save()   # .save() needs
            messages.success(request, 'Followed done', 'success')

        return redirect('account:user_profile', user_id=to_user_id)
    


class UserUnfollowView(LoginRequiredMixin, View):

    def get(self, request, to_user_id):
        following_init = FollowingInit(request, to_user_id=to_user_id)
        relation = following_init.relation
            
        if relation.exists():
            relation.delete()
            messages.error(request, 'you unFollowe this user', 'success')
        else:
            messages.success(request, 'you cant unfollow before following', 'warning')

        return redirect('account:user_profile', user_id=to_user_id)

