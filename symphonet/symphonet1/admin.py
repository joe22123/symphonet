from django.contrib import admin
from symphonet1.models import UserProfile, Album, Song, Playlist, Artist, Rating

class AlbumAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'avgRating', 'artist')
    
class SongAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'ratingScore', 'artist')
    
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user')
    
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'avgRating')
    
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'song', 'score', 'comment')
    

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Rating, RatingAdmin)
