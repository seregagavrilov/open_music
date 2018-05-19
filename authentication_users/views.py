from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import login, logout
from django.contrib.auth import authenticate
from django.shortcuts import redirect, render



def sing_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/profile/'+user.username, user_profile=user.username)
    else:
        form = UserCreationForm()
    args = {'form': form}
    return render(request, 'authentication_users/signup.html', args)


def logout_view(request):
    logout(request)
    return redirect('/')