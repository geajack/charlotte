from flask import Flask
from jinja2 import BaseLoader
from jinja2.parser import Parser
from jinja2.exceptions import TemplateNotFound

app = Flask("Charlotte")

class TemplateLoader(BaseLoader):

    def __init__(self):
        pass

    def get_source(self, environment, file_name):
        source = None
        template_path = None
        do_use_cache = self.use_cache.__get__(self, TemplateLoader)
        
        theme_folder = settings.get_theme_directory()
        if theme_folder is None:
            raise TemplateNotFound(file_name)

        template_path = str(theme_folder / "templates" / file_name)
        
        try:
            with open(template_path) as f:
                source = f.read()
        except FileNotFoundError:
            pass

        if source is None:
            template_folder = settings.get_default_template_directory()
            template_path = str(template_folder / file_name)
            with open(template_path) as f:
                source = f.read()

        return source, template_path, do_use_cache


    def use_cache(self, path=None):
        return False

app.jinja_loader = TemplateLoader()

import charlotte.routes