from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.

class Profile(models.Model):
    user    = models.OneToOneField(User,on_delete=models.CASCADE)
    image   = models.ImageField(upload_to='profile_pics/',blank=True)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self,*args,**kwargs):
        super(Profile,self).save(*args,**kwargs)
        if(self.image):
            img = Image.open(self.image.path)
            if img.width>300 or img.height>300:
                output_size = (300,300)
                img.thumbnail(output_size)
                img.save(self.image.path)
            
