from django import forms
from symphonet1.models import Rating,UserProfile, Playlist, Song
from django.contrib.auth.models import User

class ReviewForm(forms.ModelForm):
    song = forms.CharField(max_length = 128, help_text="Please write a short review (under 128 characters)")
    score = forms.IntegerField(max_value=5,min_value=0, help_text="Please enter your score (between 0-5)")

    class Meta:
        model = Rating
        fields = ('song','score')

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields =('username','email','password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ()
        
class PlaylistForm(forms.ModelForm):    
    name = forms.CharField(max_length=Playlist.NAME_MAX_LENGTH, help_text="Enter name of playlist")
    user = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=User.objects.all(), required=True)
    songs = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Song.objects.order_by('ratingScore'), label='songs')
    
    class Meta:
        model = Playlist
        fields = ('name', 'user', 'songs')
        