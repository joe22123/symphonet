from django.test import TestCase
from symphonet1.models import Song


# Create your tests here.

class SongMethodTests(TestCase):
    def check_not_negative_rating(self):
        song = Song(name='test', ratingScore=-1, album='test_album', )

