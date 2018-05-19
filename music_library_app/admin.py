from django.contrib import admin
from . import models

admin.site.register(models.Artist)
admin.site.register(models.Gener)
admin.site.register(models.Playlist)
admin.site.register(models.Song)
admin.site.register(models.Album)
