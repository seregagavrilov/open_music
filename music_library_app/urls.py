from django.urls import path,include
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import redirect_to_login
from . import views

# router = DefaultRouter()
# router.register(r'songs', views.SongViewSet)
# router.register(r'songs_search', views.SongSerchViewSet)
# router.register(r'albums', views.AlbumVievSet)
# router.register(r'artists', views.ArtistVievSet)

app_name = 'music_library_app'

urlpatterns = [
    path('<str:user_profile>',views.user_profile),
    path('login_redirect/', views.login_redirect),
    path('logout_redirect/', views.logiout_redirect),
    # path('library_info/', include(router.urls)),
    # path('songs/', views.SongViewSet.as_view()),
]
