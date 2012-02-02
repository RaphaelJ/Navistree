# -*- coding: Utf-8 -*-

import markdown

def title_to_url(title):
    """ Convertit le titre d'un article pour être utilisé dans une URL """

    return title.replace(" ", "_")

def url_to_title(url):
    """ Convertit l'url d'un article vers son nom """

    return url.replace("_", " ")

def markup(source):
    """ Applique le markup """

    return markdown.markdown(
        source,
        ['toc', 'codehilite', 'tables', 'def_list',
         'abbr', 'fenced_code', 'safe'],
        safe_mode="remove",
        output_format='xhtml1',
    )