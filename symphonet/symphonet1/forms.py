from django import forms
from symphonet1.models import Review,UserProfile
from django.contrib.auth.models import User

class ReviewForm(forms.ModelForm):
    song = forms.CharField(max_length = 128)
    rating = forms.IntegerField(max_value=5,min_value=0)

    class Meta:
        model = Review
        fields = ('song','rating')

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields =('username','email','password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website','picture')