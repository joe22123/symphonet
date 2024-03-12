from django import forms
from symphonet1.models import Rating,UserProfile
from django.contrib.auth.models import User

class ReviewForm(forms.ModelForm):
    song = forms.CharField(max_length = 128)
    score = forms.IntegerField(max_value=5,min_value=0)

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
        fields = ('user','friends')