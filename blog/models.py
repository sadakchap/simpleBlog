from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
class Post(models.Model):
    title       = models.CharField(max_length=255)
    slug        = models.SlugField(max_length=255, unique=True)
    content     = models.TextField()
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    author      = models.ForeignKey(User,on_delete=models.CASCADE)
    likes       = models.ManyToManyField(User,related_name='post_liked',blank=True)

    def __str__(self):
        return self.title
    
    def like_count(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk':self.pk})
    
    def save(self, *args, **kwargs):
        if self.slug:
            self.slug = slugify(self.title)
        return super(Post, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ('-created',)


class Comment(models.Model):
    text    = models.TextField()
    author  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_comments')
    post    = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='comments')
    reply   = models.ForeignKey('self', null=True, related_name='replies', on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}s comment on "{self.post}" '
    
    class Meta:
        ordering = ('-created',)
