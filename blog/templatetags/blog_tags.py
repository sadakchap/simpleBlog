from django import template
from django.db.models import Count
from ..models import Post

register = template.Library()

@register.inclusion_tag('blog/latest_post.html')
def latest_post():
    latest_post = Post.objects.all()[:3]
    return {'posts': latest_post}

@register.inclusion_tag('blog/latest_post.html')
def popular_post():
    posts = Post.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:3]
    return {'posts': posts}