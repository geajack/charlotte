from flask import Flask
from jinja2 import BaseLoader
from jinja2.parser import Parser
from jinja2.exceptions import TemplateNotFound
from werkzeug.wsgi import DispatcherMiddleware

from charlotte.client import application as client_app

flask_app = Flask("Charlotte")

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

flask_app.jinja_loader = TemplateLoader()

app = flask_app
from charlotte import settings

if settings.is_client_enabled():
    application = DispatcherMiddleware(
        flask_app,
        {
            "/admin": client_app
        }
    )
else:
    application = flask_app

import charlotte.routes