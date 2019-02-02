import pathlib

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

CONFIG_PATH = str(get_charlotte_root() / "charlotte.config")

try:
    config_file = ConfigParser()
    config_file.read(CONFIG_PATH)
except:
    app.logger.error("No charlotte.config file found")
    config_file = None