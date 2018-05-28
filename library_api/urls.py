from django.urls import path, include
from . import views

app_name = 'library_api'

urlpatterns = [
    path('api_v1/', include([
        path('usersongs/', views.UserSongsList.as_view(), name='usersongs'),
        path('usersongs/<pk>/',views.UserSong.as_view(),name='usersong'),
        path('useralbums/', views.AlbumUserList.as_view()),
        path('userartists/', views.ArtistUserList.as_view()),
        path('userplaylist/', views.PlaylisttUserList.as_view()),
        path('playlistsong/<id_playlist>/<id_songs>/', views.PlaylistSong.as_view()),
        path('playlistsong/<id_playlist>/', views.PlaylistSongs.as_view()),
        path('songs/', views.SongList.as_view(), name='songs'),
    ])),
]