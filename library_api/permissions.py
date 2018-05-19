from rest_framework import permissions
from music_library_app.models import User


class is_playlist_owner(permissions.BasePermission):
    # FOR DELETE PLAYLISTS OR DELETE MUSIC FROM PLAYLISTS
    # FOR UPDATE PLAYLIST'
    def has_object_permission(self, request, view, obj):
        return request.user.username == obj.owner


class is_playlist_owner_or_shared_user(permissions.BasePermission):
    # FOR READ PLAYLISTS
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        return False



