from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required


def index(request):
    if request.user.is_authenticated:
        return redirect('/profile/login_redirect/')
    return render(request, 'music_project/index.html')


def redirect_index(request):
   return redirect('index/')