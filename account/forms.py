from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserRegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))


    # field validation, prevent from same username or email
    # run when is_valid() is called
    # def clean_<filed_name>:
    
    def clean_email(self):
        # the same clean_data in form
        email = self.cleaned_data['email']
        # exists() just return true or false not all data,(is optimized)
        user = User.objects.filter(email=email).exists()

        if user:
            raise ValidationError('the emial already exists')
        # is required to return email
        return email
    
    
    def clean_username(self):
    # the same clean_data in form
        username = self.cleaned_data['username']
        # exists() just return true or false not all data,(is optimized)
        user = User.objects.filter(username=username).exists()

        if user:
            raise ValidationError('the username already exists')
        # is required to return email
        return username
    


    # validation fields that are related to each other
    # overrideing the clean method

    def clean(self):
        cd = super().clean()
        p1 = cd.get('password')
        p2 = cd.get('confirm_password')
        
        if p1 and p1 and p1 != p2:
            # validation on over form not specific fields
            raise ValidationError('passwords must match')
