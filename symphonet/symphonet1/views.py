from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'symphonet/index.html')

def about_us(request):

    return render(request, 'symphonet/about_us.html')

def account(request):
    return render(request, 'symphonet/account.html')

def user_reviews(request):
    return render(request, 'symphonet/my_reviews.html')

def user_playlists(request):
    return render(request, 'symphonet/playlists.html')
