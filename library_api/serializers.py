from rest_framework import serializers

from  music_library_app import models
from .serializer_helpers import get_user_names_for_curent_song, get_sharing_user_names_for_curent_playlist


class AlbumsSerializer(serializers.ModelSerializer):
    year = serializers.DateField

    class Meta:
        model = models.Album
        fields = ('id', 'name', 'year', 'artist')
        lookup_field = 'id'


class SongsSerializer(serializers.ModelSerializer):
    album = serializers.SerializerMethodField()
    artist = serializers.SerializerMethodField()

    def get_album(self, obj):
        return obj.album.name

    def get_artist(self, obj):
        return obj.artist.name

    def get_users(self, obj):
        return get_user_names_for_curent_song(obj.id)

    class Meta:
        model = models.Song
        fields = ('id', 'name', 'artist', 'album', 'last_play', 'file_path')
        lookup_field = 'id'


class ArtistsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Artist
        fields = ('id', 'name', 'country', 'city', 'bio')


class PlaylistsSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()

    def get_user(self, obj):
        return get_sharing_user_names_for_curent_playlist(obj.id)

    def get_owner(self, obj):
        return obj.owner.username

    class Meta:
        model = models.Playlist
        fields = ('id', 'user', 'owner', 'name', 'songs')
