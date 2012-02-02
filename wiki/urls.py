# -*- coding: Utf-8 -*-

from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to

import views

urlpatterns = patterns('',
    url(r'^$', redirect_to, {
        'url': '/wiki/article/Home/'
    }, name="wiki"),
    url(r'^article/$', redirect_to, {
        'url': '/wiki/article/Home/'
    }),
  
    url(r'^articles/$',
        views.articles, name="wiki-articles"
    ),
    
    url(r'^articles/recent/$',
        views.articles, {
            'recent': True
        }, name="wiki-recent"
    ),

    url(r'^article/([A-Z0-9][a-zA-Z0-9_]{0,127})/$',
        views.article, name="wiki-article"
    ),
    url(r'^article/([A-Z0-9][a-zA-Z0-9_]{0,127})/(\d+)/$',
        views.article, name="wiki-article-revision"
    ),

    url(r'^article/([A-Z0-9][a-zA-Z0-9_]{0,127})/edit/$',
        views.edit, name="wiki-edit"
    ),
    url(r'^article/([A-Z0-9][a-zA-Z0-9_]{0,127})/(\d+)/edit/$',
        views.edit, name="wiki-edit-revision"
    ),
    
    url(r'^article/([A-Z0-9][a-zA-Z0-9_]{0,127})/revisions/$',
        views.revisions, name="wiki-revisions"
    ),
    
    url(r'^article/([A-Z0-9][a-zA-Z0-9_]{0,127})/(\d+)/diff/$',
        views.differences, name="wiki-differences-revision"
    ),

    url(r'^article/([a-zA-Z0-9_ ]{1,128})/$',
        views.rewrite_name, name="wiki-article-rewrite"
    ),
)