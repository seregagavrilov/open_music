from django.urls import path, include
from django.contrib import admin
from . import views


app_name = 'music_library_app'

urlpatterns = [
    path('<str:user_profile>',views.user_profile),
    path('login_redirect/', views.login_redirect),
    path('logout_redirect/', views.logiout_redirect),
]

