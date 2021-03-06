# -*- coding: utf-8 -*-

import uuid

from django.contrib import auth
from django.contrib import messages
from apps.userprofile.models import SiteUser
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect


from apps.authentication.forms import (LoginForm, RegisterForm,
                            RecoveryForm, ChangePasswordForm)
from apps.authentication.models import RegisterToken
from django.conf import settings


def login(request, event=None):
    redirect_url = request.REQUEST.get('next', '')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.login(request):
            messages.success(request, 'You have successfully logged in.')
            if redirect_url:
                return HttpResponseRedirect(redirect_url)
            return redirect('root', event=event)
        else: 
            form = LoginForm(request.POST, auto_id=True)
    else:
        form = LoginForm()

    response_dict = {'form': form, 'next': redirect_url, 'event': event}
    return render(request, 'auth/login.html', response_dict)


def logout(request, event=None):
    auth.logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('root', event=event)


def register(request, event=None):
    if request.user.is_authenticated():
        messages.error(request, 'You cannot be logged in when registering.')
        return redirect('root', event=event)
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                cleaned = form.cleaned_data

                # Create user
                user = SiteUser(
                    username=cleaned['username'].lower(),
                    nickname=cleaned['username'].lower(),
                    first_name=cleaned['first_name'],
                    last_name=cleaned['last_name'],
                    email=cleaned['email'].lower(),
                    date_of_birth=cleaned['date_of_birth'],
                    zip_code=cleaned['zip_code'],
                    address=cleaned['address'],
                    phone=cleaned['phone'],
                    skype=cleaned['skype'],
                    steam=cleaned['steam'],
                    town=cleaned['town'],
                    country=cleaned['country'],
                    # image=cleaned['image'],
                )
                user.set_password(cleaned['password'])
                user.is_active = False
                user.save()
                user.setNameNotRetard()

                # Create the registration token
                token = uuid.uuid4().hex
                rt = RegisterToken(user=user, token=token)
                rt.save()

                email_message = u"""
Du har registrert en konto på dfektlan.no.

For å bruke denne kontoen må du aktivere den. Du kan aktivere den ved å besøke linken under.

http://%s/%s/auth/verify/%s/

Aktiveringslinken er kun aktiv i 24 timer, etter dette vil du måtte bruke Reset Password for
å få en ny link.
""" % (request.META['HTTP_HOST'], event, token)

                send_mail('Verify your account', email_message, settings.REGISTER_FROM_MAIL, [user.email, ])

                messages.success(request, 'Registration successful. Check your email for verification instructions.')

                return redirect('root', event=event)
            else:
                form = RegisterForm(request.POST, auto_id=True)
        else:
            form = RegisterForm()

        return render(request, 'auth/register.html', {'form': form, 'event': event, })


def verify(request, token=None, event=None):
    if request.user.is_authenticated():
        return redirect('root', event=event)
    else:
        rt = get_object_or_404(RegisterToken, token=token)
        
        if rt.is_valid:
            user = getattr(rt, 'user')

            user.is_active = True
            user.save()
            rt.delete()

            messages.success(request, "User %s successfully activated. You can now log in." % user.username)

            return redirect('auth_login', event=event)
        else:
            messages.error(request, "The token has expired. Please use the password recovery to get a new token.")
            return redirect('root', event=event)        
            

def recover(request, event=None):
    if request.user.is_authenticated():
        return redirect('root', event=event)
    else:
        if request.method == 'POST':
            form = RecoveryForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email'].lower()
                users = SiteUser.objects.filter(email=email)

                if len(users) == 0:
                    messages.error(request, "That email is not registered.")
                    return redirect('root', event=event)

                user = users[0]
                user.save()
    
                # Create the registration token
                token = uuid.uuid4().hex
                rt = RegisterToken(user=user, token=token)
                rt.save()

                email_message = u"""
You have requested a password recovery for the account bound to %s.

Username: %s

If you did not ask for this password recovery, please ignore this email.

Otherwise, click the link below to reset your password;
http://%s/%s/auth/set_password/%s/

Note that tokens have a valid lifetime of 24 hours. If you do not use this
link within 24 hours, it will be invalid, and you will need to use the password
recovery option again to get your account verified.
""" % (email, user.username, request.META['HTTP_HOST'], event, token)


                send_mail('Account recovery', email_message, settings.REGISTER_FROM_MAIL, [email,])

                messages.success(request, 'A recovery link has been sent to %s.' % email)

                return redirect('root', event=event)
            else:
                form = RecoveryForm(request.POST, auto_id=True)
        else:
            form = RecoveryForm()

        return render(request, 'auth/recover.html', {'form': form, 'event': event})


def users(request, event=None):
    u = SiteUser.objects.all()

    return render(request, 'auth/users.html', {'u': u, 'event': event})


def set_password(request, token=None, event=None):
    if request.user.is_authenticated():
        return redirect('root', event=event)
    else:
        rt = get_object_or_404(RegisterToken, token=token)

        if rt.is_valid:
            if request.method == 'POST':
                form = ChangePasswordForm(request.POST, auto_id=True)
                if form.is_valid():
                    user = getattr(rt, 'user')

                    user.is_active = True
                    user.set_password(form.cleaned_data['new_password'])
                    user.save()

                    rt.delete()

                    messages.success(request, "User %s successfully had it's password changed. You can now log in." % user)

                    return redirect('root', event=event)
            else:

                form = ChangePasswordForm()

                messages.success(request, "Token accepted. Please insert your new password.")

            return render(request, 'auth/set_password.html', {'form': form, 'token': token, 'event': event})

        else:
            messages.error(request, "The token has expired. Please use the password recovery to get a new token.")
            return redirect('root', event=event)
