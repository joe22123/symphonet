import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'symphonet.settings')

import django
django.setup()
from symphonet1.models import UserProfile, Album, Song, Playlist, Artist, Rating

def populate():
    
    # This would ideally be the naive solution to add a large amount of songs
    # into the database.
    # dataset = open('dataset.csv', 'r', encoding='utf-8')
    
    # for row in dataset:
    #     row = row.split(',')
    #     row[2] = row[2].split(';')
    #     if len(row[2]) == 1:
    #         name = row[2][0]
    #         artist = add_artist(name)
    #         album = add_album(row[3], artist)
    #         song = add_song(row[4], album, artist)
    
    # For the sake of saving time in populating the database
    # this will be used instead
    
    noah_songs = [{'name': 'Stick Season',
                   'album': 'Stick Season'}]
    
    sophie_songs = [{'name': 'Murder On The Dancefloor',
                     'album': 'Read My Lips'}]
    
    benson_songs = [{'name': 'Beautiful Things',
                     'album': 'Beautiful Things'}]
    
    tatemcrae_songs = [{'name': 'greedy',
                        'album': 'Think Later'}]
    
    natasha_songs = [{'name': 'Unwritten',
                      'album': 'Unwritten'}]
    
    sara_songs = [{'name': 'Bored',
                   'album': 'Bored'},
                  {'name': 'Freeze',
                   'album': 'Struck by Lightning'},
                  {'name': 'Home for the Summer',
                   'album': 'Camera Shy'},
                  {'name': 'Is There Anything Else?',
                   'album': 'Is There Anything Else?'}]
    
    artists = {'Noah Kahan': {'songs': noah_songs},
               'Sophie Ellis-Bextor': {'songs': sophie_songs},
               'Benson Boone': {'songs': benson_songs},
               'Tate McRae': {'songs': tatemcrae_songs},
               'Natasha Bedingfield': {'songs': natasha_songs},
               'Sara Kays': {'songs': sara_songs}}
    
    # Adds each artist
    # adds songs by that artist
    for artist, artist_data in artists.items():
        a =  add_artist(artist)
        for s in artist_data['songs']:
            add_song(a, s['name'])
            
    for a in Artist.objects.all():
        for s in Song.objects.filter(artist=a):
            print(f'- {a}:{s}')
            
def add_artist(name):
    a = Artist.objects.get_or_create(name=name)[0]
    a.save()
    return a

def add_song(artist, name):
    s = Song.objects.get_or_create(artist=artist, name=name)[0]
    s.save()
    return s

if __name__ == '__main__':
    print('Starting symphonet population script')
    populate()