import pathlib
import shutil

import yaml

from charlotte import app
from charlotte import api

class Format:

    def __init__(self, identifier, name, renderer_name, description):
        self.identifier = identifier
        self.name = name
        self.renderer_name = renderer_name
        self.description = description

    def as_api_entity(self):
        return {
            "identifier": self.identifier,
            "name": self.name,
            "description": self.description
        }

def is_password_correct(password):
    try:
        config = get_config()
        stored_password = config["blog"]["password"]
        if password == stored_password:
            return True
        else:
            return False
    except Exception as exception:
        app.logger.error("Could not get password from charlotte.config file: {}".format(exception))
        return None

def get_format(identifier):
    try:
        formats = get_formats()
        for format_object in formats:
            if identifier == format_object.identifier:
                return format_object
        return None
    except Exception as exception:
        app.logger.error("Could not get formats from charlotte.config file: {}".format(exception))
        return None

def get_formats():
    try:
        config = get_config()
        yaml_formats = config["formats"]
        formats = []
        for yaml_format in yaml_formats:
            identifier = yaml_format["identifier"]
            name = yaml_format["name"]
            renderer_name = yaml_format["renderer"]
            description = yaml_format["description"]
            formats.append(Format(identifier, name, renderer_name, description))
        return formats
    except Exception as exception:
        app.logger.error("Could not get formats from charlotte.config file: {}".format(exception))
        return []

def get_blog_name():
    try:
        config = get_config()
        return config["blog"]["name"]
    except:
        app.logger.error("Could not read 'Blog Name' key in charlotte.config file")
        return "A Charlotte Blog"

def get_charlotte_root():
    return pathlib.Path(__file__).parent.parent

def get_config():
    CONFIG_PATH = get_charlotte_root() / "charlotte.config"
    try:
        with open(CONFIG_PATH, "r") as config_file:
            config = yaml.load(config_file)
    except Exception as exception:
        app.logger.error("Could not load charlotte.config: {}".format(exception))
        config = None

    return config