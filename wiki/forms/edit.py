# -*- coding: Utf-8 -*-

from django import forms

class EditArticle(forms.Form):
    content = forms.CharField(
        label="Contenu de l'article",
        help_text="""Le contenu de l'article peut être formatté en utilisant
            les marqueurs syntaxiques de
            <a href="http://daringfireball.net/projects/markdown/syntax">
            Markdown</a>.""",
        widget=forms.widgets.Textarea(
            attrs={ 'rows': 40, 'cols': 75 }
        )
    )