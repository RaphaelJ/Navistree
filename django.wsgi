#!/usr/bin/env python2

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'navistree.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
