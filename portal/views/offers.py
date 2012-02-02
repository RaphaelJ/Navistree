# -*- coding: Utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext

from navistree.models import Version

def offers(request):
    #vers = {
        #"linux": "2.6.37-ARCH",
        #"ruby": "1.9.2",
        #"rails": "3.0.3",
        #"python2": "2.7.1",
        #"python3": "3.1.3",
        #"django": "1.2.4",
        #"mono": "2.8.2",
        #"php": "5.3.5",
        #"pgsql": "9.0.3",
        #"sqlite": "3.7.5",
        #"mysql": "5.5.9"
    #}
    #for k, v in vers.items():
        #Version(software=k, version=v).save()

    versions = { v.software: v.version for v in Version.objects.all() }

    return render_to_response('portal/offers.html', {
        'page': 'offers',
        'user': request.user,
    
        'versions': versions
    }, context_instance=RequestContext(request))
