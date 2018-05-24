from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from . import views
#import debug_toolbar

urlpatterns = [
    path('', views.redirect_index),
    path('index/', views.index),
    path('admin/', admin.site.urls),
    path('authentication/', include('authentication_users.urls')),
    path('profile/', include('music_library_app.urls')),
    path('library_api/', include('library_api.urls', namespace = 'library_api')),
    #path('oauth_api/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
