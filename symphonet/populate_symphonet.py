import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'symphonet.settings')

import django
django.setup()
from symphonet1.models import UserProfile, Album, Song, Playlist, Artist, Rating

def populate():
    
    noah_songs = [{'name': 'Stick Season',
                   'albumID': ''}]
    
    sophie_songs = [{'name': 'Murder on the dancefloor',
                     'albumID': ''}]
    
    benson_songs = [{'name': 'Beautiful Things',
                     'albumID': ''}]
    
    tatemcrae_songs = [{'name': 'greedy',
                        'albumID': ''}]
    
    natasha_songs = [{'name': 'Unwritten',
                      'albumID': ''}]
    
    sara_songs = [{'name': 'Bored',
                   'albumID': ''},
                  {'name': 'Freeze',
                   'albumID': ''},
                  {'name': 'Home for the Summer',
                   'albumID': ''},
                  {'name': 'Is There Anything Else?',
                   'albumID': ''}]
    
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