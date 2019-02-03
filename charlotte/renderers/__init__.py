import importlib

from charlotte.renderers import mathdown, plain
from charlotte import settings

def get_renderer(format_identifier):
    format_object = settings.get_format(format_identifier)
    renderer_name = format_object.renderer_name
    return importlib.import_module("charlotte.renderers." + renderer_name)