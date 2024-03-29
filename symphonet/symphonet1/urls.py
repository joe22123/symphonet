from django.urls import path
from django.conf.urls import url
from symphonet1 import views

app_name = 'symphonet'

urlpatterns = [
    path('', views.index, name='index'),
    path('about_us/', views.about_us, name='about_us'),
    path('account/', views.account, name='account'),
    path('songs/', views.SongListView.as_view(), name="songs"),
    path('songs/<int:page>',views.songs, name="songs_by_page"),
    path('songs/<int:songid>/reviews/', views.song_review, name='song_review'),
    path('songs/<int:songid>/make_review/', views.make_review, name='make_review'),
    path('account/myreviews', views.user_reviews, name='user_reviews'),
    path('account/myplaylists', views.playlists, name='playlists'),
    path('add_playlist/', views.add_playlist, name='add_playlist'),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('login/', views.user_login, name='user_login'),
    path('logout/',views.user_logout, name="logout"),
    path('add_friends/', views.add_friends, name='add_friends'), 
    path('add_friends_submit/', views.add_friends_submit, name='add_friends_submit'),
    path('remove_friends/', views.remove_friends, name='remove_friends'), 
    path('remove_friends_submit/', views.remove_friends_submit, name='remove_friends_submit'),
    
]