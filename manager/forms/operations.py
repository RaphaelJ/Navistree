# -*- coding: Utf-8 -*- 

from django import forms

class SendMailForm(forms.Form):    
    send_mail = forms.BooleanField(
        label="Être informé par email",
        help_text = "Un email vous sera transmis lors de la fin d'une opération.",
        required=False
    )