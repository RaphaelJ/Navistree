# -*- coding: Utf-8 -*-

import datetime

from django.shortcuts import render_to_response, redirect
from django.template.loader import render_to_string
from django.template import RequestContext
from django.core.mail import send_mail
from django.contrib.auth import get_backends, login
from django.core.urlresolvers import reverse

from navistree.accounts import forms
from navistree import settings
from navistree.models import User, UserProfile

def register(request):
    """ Formulaire d'inscription """
    
    def remove_expired():
        """ Supprime les comptes utilisateurs non activées et expirés """
        
        profiles = UserProfile.objects\
            .filter(activation_key_expire__lte=datetime.datetime.now())
        
        for p in profiles:
            p.user.delete()

    def send_register_email(user, password):
        """ Envoi l'email d'activation du compte """

        url_confirmation = "{absolute_url}{activation_view}".format(
            absolute_url=settings.ABSOLUTE_URL,
            activation_view=reverse(
                "register-activation",
                args=[user.id, user.get_profile().activation_key]
            )
        )

        email_subject = "Dernière étape pour terminer votre inscription sur Navistree.org"
        email_body = render_to_string("registration/register_email.html", {
            'user': user,
            
            'password': password,
            'url_confirmation': url_confirmation,
            'register_delay': settings.REGISTER_DELAY,
        })

        user.email_user(email_subject, email_body)
    
    if request.user.is_authenticated():
        return redirect("manager-account")
    
    if request.method == 'POST':
        remove_expired()
        form = forms.RegisterForm(request, request.POST)
        
        if form.is_valid():
            new_user = form.save()
            
            send_register_email(new_user, form.cleaned_data['password1'])
            return render_to_response("registration/register_confirm.html", {
                'page': 'register',
                'user': request.user,

                'email': new_user.email
            }, context_instance=RequestContext(request))
    else:
        form = forms.RegisterForm()
    
    return render_to_response("registration/register.html", {
        'page': 'register',
        'user': request.user,
        
        'form': form,
    }, context_instance=RequestContext(request))

def activate(request, user_id, activation_key):
    """ Activation de l'utilisateur """

    if request.user.is_authenticated():
        return redirect("manager-account")

    try:
        profile = UserProfile.objects.get(
            user__id=user_id,
            activation_key=activation_key,
            user__is_active=False
        )

        profile.activate()

        backend = get_backends()[0]
        profile.user.backend = "{0}.{1}".format(
            backend.__module__, backend.__class__.__name__
        )
        login(request, profile.user)

        return redirect("manager-account")
    except:
        return render_to_response("error.html", {
            'page': 'register',
            'user': request.user,
            
            'message': """
                Nous n'avons pas pu activer votre compte.<br />
                Les comptes ne sont activables que durant {0} heures. Après ce délai,
                vous devez vous réinscrire à nouveau.
            """.format(settings.REGISTER_DELAY)
        }, context_instance=RequestContext(request))