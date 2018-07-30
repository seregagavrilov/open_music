from django.http import HttpResponse
from django.contrib.auth.views import login, logout
from django.shortcuts import redirect, render
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


def sing_up(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            curent_site = get_current_site(request)
            message = render_to_string('authentication_users/acc_active_email.html', {
                'user': user,
                'domain': curent_site,
                'uid': str(user.pk),
                'token': account_activation_token.make_token(user)
            })
            mail_subject = 'Activate your blog account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            # send_mail(mail_subject, message, 'inkine.sg@gmail.com', [to_email])
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    args = {'form': form}
    return render(request, 'authentication_users/signup.html', args)


def activate(request, uidb64, token):

    try:
        user = User.objects.get(pk=int(uidb64))
    except(TypeError, ValueError, OverflowError) as a:
        print(a)
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def logout_view(request):
    logout(request)
    return redirect('/')
