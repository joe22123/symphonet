from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

def limit(value):
    if value >6 and value >0:
        raise ValidationError("please enter a number less than 5")
  
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    
    friends = models.ManyToManyField("self", blank=True)
    
    def __str__(self):
        return self.user.username

class Artist(models.Model):
    NAME_MAX_LENGTH = 30
    
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    avgRating = models.FloatField(default=0)
    
    def __str__(self):
        return self.name

class Album(models.Model):
    NAME_MAX_LENGTH = 50
    
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    coverArt = models.ImageField(upload_to='AlbumCovers/', blank=True)
    avgRating = models.FloatField(default=0)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name} by {self.artist}"
    
class Song(models.Model):
    NAME_MAX_LENGTH = 30
    
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    ratingScore = models.FloatField(default=0)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, blank=True, null=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Playlist(models.Model):
    NAME_MAX_LENGTH = 30
    
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    songs = models.ManyToManyField(Song)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Rating(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='ratings')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.TextField()
    
    class Meta:
        # Ensuring that a user can only rate a song once
        unique_together = ('user', 'song')
    
    def __str__(self):
        return f"{self.score}/5 by {self.user} for {self.song}"
    

