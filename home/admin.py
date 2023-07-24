from django.contrib import admin

from .models import Post, Comment, Like

@admin.register(Post) # first way
class PostAdmin(admin.ModelAdmin):
    # to show fields in admin panel
    list_display = ('user', 'slug', 'updated')
    search_fields = ('slug', 'body')
    list_filter = ('updated', 'created')
    # to pre_complete slug field
    prepopulated_fields = {'slug': ('body',)}
    # insted drop down menu for author(user), use user id
    raw_id_fields = ('user',)

# admin.site.register(Post, PostAdmin) # second way to show PostAdmin


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created', 'is_reply')
    raw_id_fields = ('user', 'post', 'reply')



admin.site.register(Like)

