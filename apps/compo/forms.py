# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from apps.userprofile.models import SiteUser

#USERS = []
#for user in SiteUser.objects.all():
#    USERS.append(user)

class RegisterTeamForm(forms.Form):
    teamname = forms.CharField(label='Lagnavn', max_length=30)
    username = forms.ModelMultipleChoiceField(SiteUser.objects.all())
    #username = forms.ModelChoiceField(SiteUser.objects.all(), label='Brukernavn')
    #username = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=USERS)
