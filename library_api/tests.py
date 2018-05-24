from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from music_library_app import models
from django.urls import reverse
from django.contrib.auth.models import User
from .serializers import SongsSerializer

class LibraryTestsCase(APITestCase):
    def setUp(self):
        self.new_user = User.objects.create_user(username="user", password='123')
        artist = models.Artist.objects.create(name='testArtist')
        album = models.Album.objects.create(name='testAlbum', year='1999-01-01')
        self.song = models.Song.objects.create(name='test1', artist_id=artist.id, album_id=album.id)
        self.song.user.add(self.new_user)

    def test_get_user_song(self):
        """
        Ensure we can get songs from our REST API
        """
        self.client = APIClient()
        self.client.login(username='user', password='123')
        song = models.Song.objects.get(pk=self.song.id)
        serilaizer = SongsSerializer(song)
        res = self.client.get(reverse('library_api:usersong', args = [self.song.pk]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serilaizer.data)

    def test_get_user_songs(self):
        """
        Ensure we can get songs for user from our REST API
        """
        self.client = APIClient()
        self.client.login(username='user', password='123')
        song = models.Song.objects.all()
        res = self.client.get(reverse('library_api:usersongs'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
