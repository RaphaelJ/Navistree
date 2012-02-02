# -*- coding: Utf-8 -*-

from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from navistree.models import Domain, Host
from navistree.manager import forms

@login_required
def domains(request):
    """ Liste les domaines de l'utilisateur """

    if request.method == 'POST':
        form = forms.Domain(
            request.POST, instance=Domain(user=request.user)
        )

        if form.is_valid():
            form.save()

            form = forms.Domain()
    else:
        form = forms.Domain()
        domain_added = False

    shared_hosts = Host.objects \
                    .exclude(domain__user=request.user) \
                    .filter(user=request.user)

    return render_to_response("manager/domains.html", {
        'page': 'manager',
        'manager_page': 'domains',
        'user': request.user,

        'shared_hosts': shared_hosts,
        'domains': request.user.domains.all(),
        'new_domain_form': form,
    }, context_instance=RequestContext(request))

@login_required
def domain(request, domain_id, delete=False):
    """ Liste les hôtes d'un domaine de l'utilisateur """

    d = Domain.objects.get(id=domain_id, user=request.user)
   
    if delete:
        d.delete()

        return redirect("manager-domains")
    else:
        if request.method == 'POST':
            form = forms.Host(
                request.POST,
                instance=Host(user=request.user, domain=d)
            )

            if form.is_valid():
                form.save()

                form = forms.Host()
                host_added = True
            else:
                host_added = False
        else:
            form = forms.Host()
            host_added = False

        return render_to_response("manager/domain.html", {
            'page': 'manager',
            'manager_page': 'domains',
            'user': request.user,

            'domain': d,
            'hosts': d.hosts.all(),
            'new_host_form': form,
        }, context_instance=RequestContext(request))

@login_required
def host(request, host_id, delete=False):
    """ Permet la modification ou la suppression d'une hôte """

    if delete:
        host = Host.objects.get(domain__user=request.user, id=host_id)
    
        domain_id = host.domain.id

        host.delete()

        return redirect("manager-domains-hosts", domain_id)
    else:        
        host = Host.objects.get(user=request.user, id=host_id)

        shared_host = host.domain.user != request.user
        
        if request.method == 'POST':
            form = forms.Host(
                request.POST,
                instance=host,
                can_change_hostname=not shared_host
            )

            if form.is_valid():
                form.save()

                if shared_host:
                    return redirect("manager-domains")
                else:
                    return redirect("manager-domains-hosts", host.domain.id)
        else:
            form = forms.Host(
                instance=host,
                can_change_hostname=not shared_host,
            )
        
        return render_to_response("manager/host.html", {
            'page': 'manager',
            'manager_page': 'domains',
            'user': request.user,

            'host': host,
            'host_form': form,
        }, context_instance=RequestContext(request))