from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to

import views

urlpatterns = patterns('',
    url(r'^$', redirect_to, {
        'url': '/manager/account/'
    }, name="manager"),

    url(r'^account/$', direct_to_template, {
        'template': "manager/account.html"
    }, name="manager-account"),
    
    url(r'^domains/$', views.domains, name="manager-domains"),

    url(r'^domains/(\d+)/$',
        views.domain, name="manager-domains-hosts"
    ),
    url(r'^domains/(\d+)/delete/$',
        views.domain, name="manager-domains-delete",
        kwargs={ 'delete': True },
    ),
    
    url(r'^domains/host/(\d+)/$',
        views.host, name="manager-domains-host"
    ),
    url(r'^domains/host/(\d+)/delete/$',
        views.host, name="manager-domains-host-delete",
        kwargs={ 'delete': True },
    ),
    
    url(r'^databases/$', direct_to_template, {
        'template': "manager/account.html"
    }, name="manager-databases"),

    url(r'^operations/$',
        views.operations, name="manager-operations"),
)