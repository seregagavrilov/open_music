from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

@login_required(login_url='/authentication/login')
def login_redirect(request):
    return redirect('/profile/'+request.user.username, user_profile=request.user.username)


def logiout_redirect(request):
    return redirect('/')

@login_required(login_url='/authentication/login')
def user_profile(request, user_profile):
    if request.user.username == user_profile:
        context = {'user_profile': user_profile}
        return render(request, 'music_library_app/user.html', context)
    else:
        return redirect('/authentication/login/')
