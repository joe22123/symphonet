from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'symphonet/index.html')

def about_us(request):

    return render(request, 'symphonet/about_us.html')

