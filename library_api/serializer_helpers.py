from django.contrib.auth.models import User
from music_library_app.models import Playlist
import datetime


def get_user_names_for_curent_song(song_id):
    return User.objects.filter(song__id=song_id).values_list('username', flat=True)


def get_sharing_user_names_for_curent_playlist(playlist_id):
    return Playlist.objects.filter(pk=playlist_id).prefetch_related("user").values_list("user__username", flat=True)

# def get_year_from_data(current_date):
#     d = dateutil.parser.parse(str(current_date))
#     return d.year
