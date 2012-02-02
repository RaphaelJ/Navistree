# -*- coding: Utf-8 -*-

from django.shortcuts import redirect

def home(request):
    if request.user.is_authenticated():
        return redirect("manager-account")
    else:
        return redirect("offers")