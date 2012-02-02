# -*- coding: Utf-8 -*- 

from django import forms

from navistree import models

class Domain(forms.ModelForm):
    class Meta:
        model = models.Domain
        exclude = ("user", "icon")

class Host(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if "can_change_hostname" in kwargs:
            can_change_hostname = kwargs["can_change_hostname"]
            del kwargs["can_change_hostname"]
        else:
            can_change_hostname = True
        
        super(Host, self).__init__(*args,**kwargs)

        if not can_change_hostname:
            del self.fields["name"]
    
    def clean(self):
        # La contrainte du nom d'hôte unique n'est pas validée
        # par le ModelForm si le domaine est exclu.

        cleaned_data = self.cleaned_data

        if "name" in self.fields:
            host_exists = models.Host.objects.filter(
                    domain=self.instance.domain, name=cleaned_data['name']
                ).exists()

            if host_exists:
                raise forms.ValidationError("Ce nom d'hôte existe déjà.")

        return cleaned_data
    
    class Meta:
        model = models.Host
        exclude = ("domain", "user", "icon")