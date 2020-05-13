from django.contrib import admin
from .models import Article, Comment, Hashtag

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'image', 'image_thumbnail', 'created_at', 'updated_at', 'user', )

class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'article', 'user', 'created_at', 'parent',)

class HashtagAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Hashtag, HashtagAdmin)