# -*- coding: Utf-8 -*-

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from navistree.models import UserChange, DomainChange, HostChange
from navistree.manager import forms

@login_required
def operations(request):
    """ Liste les opérations de l'utilisateur """

    profile = request.user.get_profile()

    if request.method == 'POST':
        form = forms.SendMailForm(
            request.POST
        )

        if form.is_valid():
            profile.email_after_operation = form.cleaned_data["send_mail"]
            profile.save()            
    else:
        form = forms.SendMailForm({
            'send_mail': profile.email_after_operation,
        })

    operations_user = UserChange.objects \
        .filter(user=request.user) \
        .all()[:20]
    operations_domains = DomainChange.objects \
        .filter(domain__user=request.user) \
        .all()[:20]
    operations_hosts = HostChange.objects \
        .filter(host__user=request.user) \
        .all()[:20]
    
    return render_to_response("manager/operations.html", {
        'page': 'manager',
        'manager_page': 'operations',
        'user': request.user,

        'form': form,
        'operations_user': operations_user,
        'operations_domains': operations_domains,
        'operations_hosts': operations_hosts
    }, context_instance=RequestContext(request))