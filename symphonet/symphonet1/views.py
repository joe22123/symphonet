from django.shortcuts import render,redirect
from django.http import HttpResponse
from symphonet1.models import Song, Artist, Album
from symphonet1.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required




def index(request):
    top_artists = Artist.objects.order_by('-avgRating')[:5]
    top_albums = Album.objects.order_by('-avgRating')[:5]
    top_songs = Song.objects.order_by('-ratingScore')[:5]
    return render(request, 'symphonet/index.html', {'artists': top_artists, 'albums': top_albums, 'songs': top_songs})

def about_us(request):

    return render(request, 'symphonet/about_us.html')

def account(request):
    return render(request, 'symphonet/account.html')

def user_reviews(request):
    #topFiveSongs = Song.objects.order_by('-ratingScore')[:5]
    context_dict = {}
    #context_dict['topFive'] = topFiveSongs
    return render(request, 'symphonet/my_reviews.html', context = context_dict)

def user_playlists(request):
    return render(request, 'symphonet/playlists.html')

def sign_up(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)

        if user_form.is_valid() :
            user = user_form.save()
            user.set_password(user.password)
            registered = True
            user.save()   
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
        
    
    context_dict ={'user_form':user_form,
                   'registered':registered}

    return render(request, 'symphonet/sign_up.html', context = context_dict)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)

        if user:
            if user.is_active:
                login(request,user)
                return (redirect(reverse('symphonet:index')))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render (request, 'symphonet/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('symphonet:index'))
