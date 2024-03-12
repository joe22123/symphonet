from django.shortcuts import render
from django.http import HttpResponse
from symphonet1.models import Song
from symphonet1.forms import UserForm, UserProfileForm


def index(request):
    return render(request, 'symphonet/index.html')

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
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    context_dict ={'user_form':user_form,
                   'profile_form': profile_form,
                   'registered':registered}

    return render(request, 'symphonet/sign_up.html', context = context_dict)

def login(request):
    return render(request, 'symphonet/login.html')
