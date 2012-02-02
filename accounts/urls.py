from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth.views import \
    login, logout, password_reset, password_reset_done, password_reset_confirm,\
    password_reset_complete

from views import register, activate
from forms import SetPasswordForm

urlpatterns = patterns('',
    url(r'^register/$', register, name="register"),
    url(r'^register/activate/(\d{1,20})/(\d{1,20})/$', activate, name="register-activation"),
    
    url(r'^login/$', login, name="login"),

     url(r'^logout/$', logout, {
        'next_page': "/",
    }, name="logout"),
    
    url(r'^password_reset/$', password_reset, name="password-reset"),
    url(r'^password_reset/done/$', password_reset_done, name="password-reset-done"),
    url(r'^password_reset/([0-9A-Za-z]+)/(.+)/$', password_reset_confirm, {
        'set_password_form': SetPasswordForm,
    }, name="password-reset-confirm"),
    url(r'^password_reset/complete/$', password_reset_complete, name="password-reset-complete"),
)