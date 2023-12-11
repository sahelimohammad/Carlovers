from django.contrib import admin
from .models import Post , Comment , Vote , DisLike


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user' , 'slug' , 'updated' , 'created')
    search_fields = ('slug' , 'body')
    list_filter = ('updated',)
    prepopulated_fields = {'slug' : ('body',)}
    raw_id_fields = ('user',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user' , 'post' , 'created' , 'is_reply')
    raw_id_fields = ('user' , 'post' , 'reply')

admin.site.register(Vote)
admin.site.register (DisLike)

"""@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user' , 'post')
    raw_id_fields = ('user' , 'post')
"""

