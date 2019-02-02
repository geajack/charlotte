from configparser import ConfigParser

try:
    config_file = ConfigParser("charlotte.config")
except:
    # app.logger.error("No charlotte.config file found")
    config_file = None

def get_blog_name():
    try:
        return config_file.get("blog", "Blog Name")
    except:
        # app.logger.error("Could not read 'Blog Name' key in charlotte.config file")
        return "A Charlotte Blog"