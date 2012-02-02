# -*- coding: Utf-8 -*-

import os

from django import forms
from django.contrib.auth import forms as auth_forms
from django.utils.translation import ugettext_lazy as _

class SetPasswordForm(auth_forms.SetPasswordForm):
    """
        Formulaire d'enregistrement d'un nouveau mot de passe.
        Force les mots de passe de plus de 8 caractères.
    """

    new_password1 = forms.CharField(
        min_length=8,
        label=_("New password"), widget=forms.PasswordInput,
        help_text = ("Entrer un mot de passe de 8 caractères ou plus.")
    )
    new_password2 = forms.CharField(
        min_length=8,
        label=_("New password confirmation"), widget=forms.PasswordInput
    )