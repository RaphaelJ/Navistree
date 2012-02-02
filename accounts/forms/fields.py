# -*- coding: Utf-8 -*-

from django.forms import Field

from widgets import Captcha

class CaptchaField(Field):
    def __init__(self, *args, **kwargs):
        self.widget = Captcha
        super(CaptchaField, self).__init__(*args, **kwargs)

    def clean(self, values):
        challenge, response = values
        
        challenge = super(CaptchaField, self).clean(challenge)

        return challenge, response