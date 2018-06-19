from django.core.exceptions import ObjectDoesNotExist
from rest_framework import filters, permissions, generics, status, mixins
from rest_framework.response import Response

from library_api import serializers
from music_project import models
from .library_api_views_helpers import __get_user_relating_data__
from .library_api_views_helpers import get_playlist


class UserSong(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.SongsSerializer
    filter_fields = ('name', 'file_path', 'artist', 'album', 'last_play')

    def get(self, request, *args, **kwargs):
        current_aouth_user = self.request.user
        query_set_song = current_aouth_user.song_set.filter(pk=kwargs.get('pk'))or None
        if query_set_song is not None:
            serilazer = self.serializer_class(query_set_song[0])
            return Response(serilazer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, *args, **kwargs):
        query_set_song = models.Song.objects.filter(pk=kwargs.get('pk')) or None
        if query_set_song is not None:
            query_set_song[0].user.remove(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserSongsList(generics.ListCreateAPIView, mixins.DestroyModelMixin):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.SongsSerializer
    filter_fields = ('name', 'file_path', 'artist', 'album', 'last_play')

    def get_queryset(self):
        current_aouth_user = self.request.user
        return current_aouth_user.song_set.all()


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    def post(self, request, *args, **kwargs):
        id_current_song = request.data.get('id')
        query_set_song = models.Song.objects.filter(id=id_current_song) or None
        if query_set_song is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            current_song = query_set_song[0]
            current_song.user.add(request.user)
            current_song.save()
            return Response(status=status.HTTP_201_CREATED)


class AlbumUserList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.AlbumsSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'year', 'artist')

    def get_queryset(self):
        cerrent_aouth_user = self.request.user
        return __get_user_relating_data__(cerrent_aouth_user, models.Album)

    def post(self, request, *args, **kwargs):
        """
        form logic when it required
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # return self.create(request, *args, **kwargs)


class ArtistUserList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ArtistsSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'country', 'city', 'bio')

    def get_queryset(self):
        cerrent_aouth_user = self.request.user
        return __get_user_relating_data__(cerrent_aouth_user, models.Artist)

    def post(self, request, *args, **kwargs):
        """
        form logic when it required
        :param request:
        :param args:
        :param kwargs:
        :return:
        """



class PlaylisttUserList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = serializers.PlaylistsSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('owner', 'user', 'songs')

    def get_queryset(self):
        current_aouth_user = self.request.user
        # return models.Playlist.objects.filter(owner=current_aouth_user).select_related()
        return current_aouth_user.playlist_set.all().prefetch_related("user")
        # return list(chain(q1,q2))
        # return current_aouth_user.playlist_set.all().prefetch_related('songs')

    def post(self, request, *args, **kwargs):
        """
        form logic when it required
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        current_aouth_user = self.request.user
        name= request.data.get('name')
        new_playlist = models.Playlist(name=name, owner=current_aouth_user)
        new_playlist.save()
        new_playlist.user.add(current_aouth_user)
        return Response(status=status.HTTP_201_CREATED)


class PlaylistSong(generics.ListCreateAPIView):
    # permission_classes = [permissions.IsAuthenticated,]
    serializer_class = serializers.SongsSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('id', 'name', 'artist__name', 'album__name', 'last_play')

    def get(self, request, *args, **kwargs):
        song_id = kwargs.get("id_songs") or None
        playlist_id = kwargs.get("id_playlist") or None
        try:
            current_playlist = get_playlist(playlist_id)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        songqueryset = current_playlist.songs.filter(pk=song_id) or None
        if songqueryset is not None:
            serilazer = self.serializer_class(songqueryset[0])
            return Response(serilazer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def post(self, request, *args, **kwargs):
        id_songs = request.data.get("id_songs")
        id_playlist = request.data.get("id_playlist")
        try:
            current_playlist = get_playlist(id_playlist)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        songqueryset = models.Song.objects.filter(pk=id_songs) or None
        if songqueryset is not None:
            current_playlist.songs.add(songqueryset[0])
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, *args, **kwargs):
        id_songs = kwargs.get("id_songs") or None
        id_playlist = kwargs.get("id_playlist") or None
        try:
            current_playlist = get_playlist(id_playlist)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        songqueryset = models.Song.objects.filter(pk=id_songs) or None
        if songqueryset is not None:
            current_playlist.songs.remove(songqueryset[0])
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)



class PlaylistSongs(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.SongsSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('id', 'name', 'artist__name', 'album__name', 'last_play')
    lookup_url_kwarg = "id_playlist"

    def get_queryset(self):
        playlist_id = self.kwargs.get(self.lookup_url_kwarg)
        current_playlist = models.Playlist.objects.filter(pk = playlist_id) or None
        if current_playlist is not None:
            return current_playlist[0].songs.all()


class SongList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = models.Song.objects.all()
    serializer_class = serializers.SongsSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','album__name', 'artist__name','artist__country','artist__City','album__year',)
    lookup_field = "pk"

