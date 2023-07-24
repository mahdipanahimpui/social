from django.contrib import admin
from .models import Relation, Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False # delete btn in admin pannel is disabled


class ExtendedUserAdmin(UserAdmin):
    # add profile inline to extended user admin
    inlines = (ProfileInline, )

# unregister the User model
admin.site.unregister(User)
# register the extended user model
admin.site.register(User, ExtendedUserAdmin)


admin.site.register(Relation)
