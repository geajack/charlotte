import pathlib
import shutil

import yaml

from charlotte import app

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
        if not (CONFIG_PATH.exists() and CONFIG_PATH.is_file()):
            default_config = get_charlotte_root() / "resources" / "charlotte.config"
            shutil.copy(default_config, CONFIG_PATH)

        with open(CONFIG_PATH, "r") as config_file:
            config = yaml.load(config_file)
    except Exception as exception:
        app.logger.error("Could not load charlotte.config: {}".format(exception))
        config = None

    return config