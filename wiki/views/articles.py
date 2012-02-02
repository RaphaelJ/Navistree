# -*- coding: Utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext

from navistree.models import Article

def articles(request, recent=False):
    pass