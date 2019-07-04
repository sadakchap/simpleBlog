from django.contrib import admin
from .models import Post, Comment

# Register your models here.

class CommentInline(admin.StackedInline):
    model = Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','author','created','updated']
    list_filter  = ['created','updated']
    search_fields = ['title','content']
    prepopulated_fields = {'slug':('title',)}
    inlines = [CommentInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['text','author','post','created','updated']
    list_filter = ['created', 'updated']

# admin.site.register(Comment)
