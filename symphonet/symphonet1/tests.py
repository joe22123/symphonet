from django.test import TestCase, Client
from django.urls import reverse,resolve
from symphonet1.models import Song,Album,Artist, User, Rating, UserProfile
from symphonet1.views import index,about_us,account,add_friends,add_friends_submit,remove_friends,remove_friends_submit,user_reviews,song_review,make_review,user_login,sign_up


# Create your tests here.

def create_user(username,email,password,first_name,last_name):
    u = User.objects.get_or_create(username=username)[0]
    u.email = email
    u.password = password
    u.first_name = first_name
    u.last_name = last_name
    u.save()

    return u

class SongMethodTests(TestCase):

    def can_create_user(self):

        test_User = create_user('test_user','test@gmail.com','testPassword1','joe','test')

        self.assertEqual((test_User.username =='test_user'), True)
        self.assertEqual((test_User.email =='test@gmail.com'), True)
        self.assertEqual((test_User.password =='testPassword1'), True)
        self.assertEqual((test_User.first_name =='joe'), True)
        self.assertEqual((test_User.last_name =='test'), True)
        

    
    def test_user_can_add_rating(self):

        user = User.objects.create(username='test_user',email='test@gmail.com',password='testPassword1')
        test_user=UserProfile.objects.create(user=user)

        test_artist = Artist.objects.create(name='test_artist', avgRating=0)
        test_album = Album.objects.create(name='test_album', coverArt=None, avgRating=0, artist=test_artist)

        song = Song.objects.create(name='test', ratingScore=0, album=test_album, artist=test_artist)

        rating = Rating.objects.create(user=test_user,song=song,score=5,comment='test')

        self.assertGreaterEqual(song.ratingScore, 1)

class urlTests(TestCase):

    client = Client()

    def test_index_url(self):
        path = reverse('symphonet:index')
        self.assertEquals(resolve(path).func, index)

    def test_account_url(self):
        path = reverse('symphonet:account')
        self.assertEquals(resolve(path).func, account)

    def test_sign_up_url(self):
        path=reverse('symphonet:sign_up')
        self.assertEquals(resolve(path).func, sign_up)

    def test_about_us_url(self):
        path=reverse('symphonet:about_us')
        self.assertEquals(resolve(path).func, about_us)




