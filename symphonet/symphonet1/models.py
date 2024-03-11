from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# Create your models here.

def limit(value):
    if value >6 and value >0:
        raise ValidationError("please enter a number less than 5")

class Review(models.Model):
    song = models.CharField(max_length = 128)
    rating = models.IntegerField(default=0,validators = [limit])

    def __str__(self):
        return self.song
    
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
    
