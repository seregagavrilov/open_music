from django.urls import path
from django.contrib.auth.views import login, logout
from . import views

urlpatterns = [
    path('login/', login, {'template_name':'authentication_users/login.html'}, name='login'),
    path('logout/', views.logout, {'next_page': '/index'}, name='logout'),
    path('signup/', views.sing_up,  name='signup'),
    path(
        'activate/<str:uidb64>/<str:token>/',
        views.activate, name='activate'
    ),
]