# -*- coding: Utf-8 -*-

import difflib

from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from navistree.models import Article, ArticleRevision
from navistree.wiki import utils, forms

def rewrite_name(request, name):
    """ Redirige vers la page avec le nom de l'article correct """

    new_name = name.strip() # Remove edges spaces
    new_name = new_name[0].upper() + new_name[1:] # Capitalise
    new_name = new_name.replace(" ", "_") # Convert spaces

    return redirect("wiki-article", new_name)

def article(request, name_url, revision=None):
    """ Affiche le contenu d'un article """
    
    name = utils.url_to_title(name_url)

    try:
        art = Article.objects.get(name=name)

        if revision != None:
            content = utils.markup(art.revisions.get(id=revision).content)
        else:
            content = art.content
        
        return render_to_response("wiki/article.html", {
            'page': 'wiki',
            'wiki_page': 'article',
            'user': request.user,

            'article_name': name,
            'article_exists': True,
            'revision': revision,
            'content': content,
        }, context_instance=RequestContext(request))
    except:
        return render_to_response("wiki/article_not_found.html", {
            'page': 'wiki',
            'wiki_page': 'article',
            'user': request.user,

            'article_name': name,
            'article_exists': False,
        }, context_instance=RequestContext(request))

@login_required
def edit(request, name_url, revision=None):
    """ Edite le contenu d'un article """    

    name = utils.url_to_title(name_url)

    try:
        art = Article.objects.get(name=name)
        exists = True
    except:
        art = Article(name=name)
        exists = False

    if request.method == 'POST':
        form = forms.EditArticle(
            request.POST
        )

        if form.is_valid():
            content = form.cleaned_data["content"]
            content_html = utils.markup(content)
            
            if "preview" in request.POST:
                preview = content_html
            else:
                art.content = content_html
                art.save()

                revision = art.revisions.create(
                    user=request.user, content=content
                )

                return redirect("wiki-article", name)
    else:
        preview = None
        
        try: # Edition de l'article
            if revision != None:
                rev = art.revisions.get(id=revision)
            else:
                rev = art.revisions.latest("id")

            form = forms.EditArticle({
                'content': rev.content
            })
        except: # Création de l'article
            form = forms.EditArticle()
    
    return render_to_response("wiki/article_edit.html", {
        'page': 'wiki',
        'wiki_page': 'edit',
        'user': request.user,

        'article_name': name,
        'article_exists': exists,
        'revision': revision,
        'form': form,
        'preview': preview,
    }, context_instance=RequestContext(request))

def revisions(request, name_url):
    """ Affiche les révisions d'un article """

    name = utils.url_to_title(name_url)

    article = Article.objects.get(name=name)
    
    return render_to_response("wiki/article_revisions.html", {
        'page': 'wiki',
        'wiki_page': 'revisions',
        'user': request.user,

        'article_name': name,
        'article_exists': True,
        'revisions': article.revisions.all(),
    }, context_instance=RequestContext(request))
    
def differences(request, name_url, revision):
    """ Montre les différences d'une révision """
    