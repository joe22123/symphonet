from django.urls import path
from django.conf.urls import url
from symphonet1 import views

app_name = 'symphonet'

urlpatterns = [
    path('', views.index, name='index'),
    path('about_us/', views.about_us, name='about_us'),
    path('account/', views.account, name='account'),
    path('account/myreviews', views.user_reviews, name='user_reviews'),
    path('account/myplaylists', views.user_playlists, name='playlists'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('login/', views.login, name='login'),
]