from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from views import offers

urlpatterns = patterns('',
    url(r'^offers/$', offers, name="offers"),
)