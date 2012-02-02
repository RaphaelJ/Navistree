# -*- coding: Utf-8 -*-

from django.forms import widgets
from django.forms.util import flatatt
from django.utils.encoding import smart_unicode

from navistree import settings

class Captcha(widgets.Widget):
    def __init__(self, extra_attrs=None):
        attrs = {
            "rows": "3",
            'cols': "40"
        }

        if extra_attrs:
            attrs.update(extra_attrs)
        
        super(Captcha, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        value = None
        
        return (u'<script type="text/javascript" ' + \
            u'src="http://www.google.com/recaptcha/api/challenge?k={public_key}">' + \
            u'</script>' + \
            u'<noscript>' + \
            u'<iframe src="http://www.google.com/recaptcha/api/noscript?k={public_key}"' + \
            u'height="300" width="500" frameborder="0"></iframe><br />' + \
            u'<textarea name="recaptcha_challenge_field"{attrs}>' + \
            u'</textarea>' + \
            u'<input type="hidden" name="recaptcha_response_field" ' + \
            u'value="manual_challenge">' + \
            u'</noscript>').format(
                name=name,
                public_key=settings.RECAPTCHA_PUBLIC_KEY,
                attrs=flatatt(attrs)
            )

    def value_from_datadict(self, data, files, name):
        return (
            data.get("recaptcha_challenge_field", None),
            data.get("recaptcha_response_field", None)
        )