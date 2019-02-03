import pathlib
import shutil

from configparser import ConfigParser
from charlotte import app

def get_blog_name():
    try:
        config_file.read(CONFIG_PATH)
        return config_file.get("blog", "Blog Name")
    except:
        app.logger.error("Could not read 'Blog Name' key in charlotte.config file")
        return "A Charlotte Blog"

def get_charlotte_root():
    return pathlib.Path(__file__).parent.parent

CONFIG_PATH = get_charlotte_root() / "charlotte.config"

try:
    if CONFIG_PATH.exists() and CONFIG_PATH.is_file():
        config_file = ConfigParser()
        config_file.read(CONFIG_PATH)
    else:
        default_config = get_charlotte_root() / "resources" / "charlotte.config"
        shutil.copy(default_config, CONFIG_PATH)
except Exception as exception:
    app.logger.error("Could not load charlotte.config: {}".format(exception))
    config_file = None