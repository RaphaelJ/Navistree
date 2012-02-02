# -*- coding: Utf-8 -*-

import os, urllib

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

from navistree.models import UserProfile, Host, User, host_validator
from navistree import settings

from fields import CaptchaField

class RegisterForm(UserCreationForm):
    """ Formulaire d'enregistrement d'un l'utilisateur """
    
    username = forms.CharField(
        label=_("Username"), min_length=3, max_length=63,
        help_text = "Entre 3 et 63 caractères alphanumériques minuscules.\n" +
            "Ce nom d'utilisateur correspondra à votre sous-domaine " +
            "(<strong>utilisateur</strong>.navistree.org).",
        validators=[host_validator]
    )

    password1 = forms.CharField(
        min_length=8, 
        label=_("Password"), widget=forms.PasswordInput,
        help_text = ("Entrer un mot de passe de 8 caractères ou plus.")
    )
    password2 = forms.CharField(
        min_length=8, 
        label=_("Password confirmation"), widget=forms.PasswordInput,
        help_text = _("Enter the same password as above, for verification.")
    )

    first_name = forms.CharField(
        label="Prénom", max_length=30, min_length=2
    )
    last_name = forms.CharField(
        label="Nom", max_length=30, min_length=2
    )

    email = forms.EmailField(
        label="Email",
        help_text = "Enter une adresse email. Celle-ci sera utilisée pour " +
            "la validation de votre compte."
    )
    
    country = forms.CharField(
        label="Pays de résidence (facultatif)",
        max_length=64, required=False
    )

    captcha = CaptchaField(
        label="Code de vérification"
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request

        super(RegisterForm, self).__init__(*args, **kwargs)
    
    def clean_username(self):
        username = super(RegisterForm, self).clean_username()

        # Vérifie si une hote du domaine principal n'a pas le même nom
        # (mail, ns1, www, ...)
        system_hosts = (h.name for h in Host.objects.filter(domain=1).all())
        
        # Vérifie si l'utilisateur n'est pas un utilisateur système
        system_users = (line[:line.find(":")] for line in open("/etc/passwd", "r"))
        
        if username in system_hosts or username in system_users:
            raise forms.ValidationError("Ce nom d'utilisateur ne peut être utilisé.")
        else:
            return username

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cette adresse email est déjà utilisée.")
        else:
            return email

    def clean_captcha(self):
        challenge, response = self.cleaned_data['captcha']
        
        result = urllib.urlopen(
            "http://www.google.com/recaptcha/api/verify",
            urllib.urlencode({
                'privatekey': settings.RECAPTCHA_PRIVATE_KEY,
                'remoteip': self.request.META['REMOTE_ADDR'],
                'challenge': challenge,
                'response': response
            })
        ).read()

        if not result.startswith("true"):
            raise forms.ValidationError("Le code de vérification n'est pas valide.")
        else:
            return challenge, response

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)

        user.set_password(self.cleaned_data['password1'])
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        try:
            profile = user.get_profile()
        except:
            profile = UserProfile(user=user)

        profile.country = self.cleaned_data['country']
        profile.save()

        return user