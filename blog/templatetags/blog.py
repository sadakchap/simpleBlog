from django import template
from ..models import Post

register = template.Library()

def latest_post():
    return Post.objects.all()