from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from symphonet1.models import Song, Artist, Album, Rating, Playlist, UserProfile
from symphonet1.forms import UserForm, UserProfileForm, UserProfile, ReviewForm, PlaylistForm
from django.contrib.auth import authenticate, login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.template import loader
from django.contrib.auth.models import User
from django.db.models import Avg
from django.contrib import messages

SONGS_IN_PAGE = 5

def index(request):
    top_artists = Artist.objects.order_by('-avgRating')[:5]
    top_albums = Album.objects.order_by('-avgRating')[:5]
    top_songs = Song.objects.order_by('-ratingScore')[:5]
    return render(request, 'symphonet/index.html', {'artists': top_artists, 'albums': top_albums, 'songs': top_songs})

def about_us(request):

    return render(request, 'symphonet/about_us.html')

def account(request):
    # Shows all users except the current one
    context_dict={}
    users = User.objects.exclude(pk=request.user.pk)
    context_dict['users'] = users
    current_user_profile = UserProfile.objects.get(user=request.user)
    
    playlists = Playlist.objects.all().filter(user=request.user)[:5]
    ratings = Rating.objects.all().filter(user=current_user_profile)[:5]
    context_dict['playlists'] = playlists
    context_dict['ratings'] = ratings
    
    # Check if a UserProfile already exists for the user
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)
        
    friends = user_profile.friends.all()
    context_dict['friends'] = friends
    return render(request, 'symphonet/account.html', context=context_dict)

def add_friends(request):   
    users = User.objects.exclude(pk=request.user.pk)
    
    for user in users:
        try:
            UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            # If UserProfile doesn't exist, create it
            UserProfile.objects.create(user=user)

    return render(request, 'symphonet/add_friends.html', {'users': users})

def add_friends_submit(request):
    if request.method == 'POST':
        selected_friend_ids = request.POST.getlist('friends')  # Get the list of selected friend IDs from the form
        current_user_profile = UserProfile.objects.get(user=request.user)

        # Add each selected friend to the current user's friend list
        for friend_id in selected_friend_ids:
            friend_profile = UserProfile.objects.get(pk=friend_id)
            current_user_profile.friends.add(friend_profile)

        # Redirect to a success page or another page
        return redirect('symphonet:account')  # Update 'confirmation' with the appropriate URL name

    # If the request method is not POST or if there's an error, render the form page again
    users = User.objects.exclude(pk=request.user.pk)
    return render(request, 'symphonet/add_friends.html', {'users': users})

def remove_friends(request):
    current_user_profile = UserProfile.objects.get(user=request.user)
    friends = current_user_profile.friends.all()
    return render(request, 'symphonet/remove_friends.html', {'friends': friends})

def remove_friends_submit(request):
    if request.method == 'POST':
        selected_friend_ids = request.POST.getlist('friends')  # Get the list of selected friend IDs from the form
        current_user_profile = UserProfile.objects.get(user=request.user)

        # Remove each selected friend from the current user's friend list
        for friend_id in selected_friend_ids:
            friend_profile = UserProfile.objects.get(pk=friend_id)
            current_user_profile.friends.remove(friend_profile)

        # Redirect to a success page or another page
        return redirect('symphonet:account')  # Update with the appropriate URL name

    # If the request method is not POST or if there's an error, render the form page again
    return redirect('symphonet:remove_friends')

def user_reviews(request):
    context_dict = {}
    current_user_profile = UserProfile.objects.get(user=request.user)
    user_reviews = Rating.objects.filter(user=current_user_profile)
    
    context_dict['reviews'] = user_reviews
    return render(request, 'symphonet/my_reviews.html', context = context_dict)

def song_review(request, songid):
    print("Song Review View Called")  # Debugging line
    song = get_object_or_404(Song, id=songid)
    
    ratings = Rating.objects.filter(song=song)
    
    average_score = ratings.aggregate(Avg('score'))['score__avg']
    
    if average_score is None:
        average_score = "No ratings yet"

    print("Context:", {
        'song': song,
        'ratings': ratings,
        'ratingScore': average_score,
    })  # Debugging line to inspect context
    
    return render(request, 'symphonet/song_review.html', {
        'song': song,
        'ratings': ratings,
        'ratingScore': average_score,
    })

@login_required
def make_review(request, songid):
    song = get_object_or_404(Song, id=songid)
    existing_review = Rating.objects.filter(user=UserProfile.objects.get(user=request.user), song=song).first()

    if request.method == 'POST':
        if existing_review:
            messages.error(request, 'You have already reviewed this song.')
            return redirect('symphonet:song_review', songid=song.id)
        else:
            post_data = request.POST.copy()
            post_data['song'] = songid
            form = ReviewForm(post_data)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = UserProfile.objects.get(user=request.user)
            review.save()
            return redirect('symphonet:song_review', songid=song.id)
    else:
        form = ReviewForm()
    return render(request, 'symphonet/make_review.html', {'form': form, 'song': song})

class SongListView(ListView):
    paginate_by = SONGS_IN_PAGE
    model = Song
    template_name = 'symphonet/songs.html'
    
def songs(request,page):
    all_songs = Song.objects.all().order_by('ratingScore')
    paginator = Paginator(all_songs, per_page=SONGS_IN_PAGE)
    
    page_object = paginator.get_page(page)
    context_dict = {'page_obj': page_object}
    return render(request,'symphonet/songs.html', context = context_dict)

@login_required
def playlists(request):
    all_playlists = Playlist.objects.all()
    context_dict = {}
    try:
        context_dict['playlists'] = all_playlists
    except Playlist.DoesNotExist:
        context_dict['playlists'] = None
    return render(request, 'symphonet/playlists.html', context = context_dict)

@login_required
def add_playlist(request):
    if request.method == "POST":
        form = PlaylistForm(request.POST, initial={'user': request.user,'songs': None})
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('symphonet:songs'))
        else:
            print(form.errors)
    else:
        form = PlaylistForm(initial={'user': request.user, 'songs': None})
            
    context_dict = {'form': form}       
    return render(request, 'symphonet/add_playlist.html', context=context_dict)
    
def sign_up(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            registered = True
            user.save()   
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
        
    
    context_dict ={'user_form':user_form,
                   'profile_form':profile_form,
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
