from django.conf.urls.defaults import *
#from django.contrib import admin
#from django.conf import settings
from django.views.generic.simple import redirect_to, direct_to_template

import portal, accounts, manager, wiki, views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.home, name="home"),

    (r'^portal/', include(portal.urls)),

    (r'^accounts/', include(accounts.urls)),

    url(r'^manager/', include(manager.urls)),

    url(r'^wiki/', include(wiki.urls)),

    url(r'^forums/$', direct_to_template, {
        'template': "manager/account.html"
    }, name="forums"),

    url(r'^manager/logout/$', direct_to_template, {
        'template': "manager/account.html"
    }, name="manager-logout"),
)
