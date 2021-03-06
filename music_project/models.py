from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import localdate


class Artist(models.Model):
    name = models.CharField(max_length=256)
    country = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    bio = models.TextField()

    def __str__(self):
        return self.name


class Gener(models.Model):
    name = models.CharField(max_length=128)
    artists = models.ManyToManyField(Artist)

    def __str__(self):
        return self.name


class Album(models.Model):
    artist = models.ForeignKey(Artist, related_name='whose_album', on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=128)
    album_info = models.TextField(blank=True)
    year = models.DateField()

    def __str__(self):
        return self.name


class Song(models.Model):
    user = models.ManyToManyField(User,blank=True)
    name = models.CharField(max_length=128)
    artist = models.ForeignKey(Artist, related_name='artist', on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    last_play = models.DateTimeField(auto_now=True)
    file_path = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Playlist(models.Model):
    owner = models.ForeignKey(User, related_name='owner',  on_delete=models.CASCADE)
    user = models.ManyToManyField(User, blank=True)
    name = models.CharField(max_length=128)
    songs = models.ManyToManyField('Song', related_name='songs', blank=True)

    def __str__(self):
        return self.name
