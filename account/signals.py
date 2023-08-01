# for each app create a signal.py file
# dclare signal.py file to django, in app.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile




@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    if kwargs['created']: # if creating User model is OK, returns True
        Profile.objects.create(user=kwargs['instance'])



# SECOND WAY    
# instead using decorator use this function

# post_save.connect(receiver=create_profile, sender=User)