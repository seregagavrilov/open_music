from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.redirect_index),
    path('index/', views.index),
    path('admin/', admin.site.urls),
    path('authentication/', include('authentication_users.urls')),
    path('profile/', include('music_library_app.urls')),
    path('library_api/', include('library_api.urls', namespace = 'library_api')),
]
