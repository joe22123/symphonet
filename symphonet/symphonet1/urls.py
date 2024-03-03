from django.urls import path
from django.conf.urls import url
from symphonet1 import views

app_name = 'symphonet'

urlpatterns = [
    path('', views.index, name='index'),
    path('about_us/', views.about_us, name='about_us')
]