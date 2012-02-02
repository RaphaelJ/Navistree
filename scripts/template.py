#!/usr/bin/python
#-*- coding: Utf-8 -*-

import navistree

TEMPLATES_DIR = navistree.SCRIPTS_HOME + "/templates/{template}.tpl"

_templates_cache = {} # Cache le contenu des templates ouverts

class Template:
    def __init__(self, tpl):
        self.path = TEMPLATES_DIR.format(template=tpl)
        self._dic = {}

    def replace(self, dic):
        self._dic = dic;

    def generate(self):
        if self.path in _templates_cache:
            lines = _templates_cache[self.path]
        else:
            with open(self.path, 'r') as f:
                lines = list(f)
            _templates_cache[self.path] = lines

        for line in lines:
            yield line.format(**self._dic)

    def write(self, dest_path=None, dest_file=None):
        def write_in_file(f):
            for line in self.generate():
                f.write(line)

        if dest_path != None:
            with open(dest_path, 'w') as f:
                write_in_file(f)
        elif dest_file != None:
            write_in_file(dest_file)
        else:
            raise "Destination must be specified"

    def __repr__(self):
        return "<Template '{path}' instance at {id}>".format(path=self.path,
            id=id(self))