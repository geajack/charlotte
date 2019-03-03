from flask import Flask
from jinja2 import BaseLoader
from jinja2.parser import Parser
from jinja2.exceptions import TemplateNotFound

app = Flask("Charlotte")

class TemplateLoader(BaseLoader):

    def __init__(self):
        pass

    def get_source(self, environment, name):
        theme_folder = settings.get_theme_directory()
        if theme_folder is None:
            raise TemplateNotFound(name)

        template_path = theme_folder / "templates" / name
        
        try:
            with open(template_path) as f:
                return f.read(), str(template_path), self.use_cache.__get__(self, TemplateLoader)
        except FileNotFoundError:
            raise TemplateNotFound(name)

    def use_cache(self, path):
        return False

app.jinja_loader = TemplateLoader()

import charlotte.routes