import importlib

from charlotte import settings

def get_renderer(format_identifier):
    format_object = settings.get_format(format_identifier)
    renderer_name = format_object.renderer_name
    charlotte_root = settings.get_charlotte_root()
    renderer_directory = charlotte_root / "renderers"
    spec = importlib.util.spec_from_file_location("module.name", renderer_directory / (renderer_name + ".py"))
    renderer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(renderer)
    return renderer