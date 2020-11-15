from pathlib import Path
from shutil import copytree, copy
from sys import argv

from jinja2 import Template

import charlotte.articles

def init(path, name, password):
    try:
        target = Path(path)
        resources_directory = Path(__file__).parent / "resources"
        copytree(
            src=resources_directory / "renderers",
            dst=target / "renderers"
        )
        copytree(
            src=resources_directory / "themes",
            dst=target / "themes"
        )
        
        with open(resources_directory / "charlotte.config.jinja") as file:
            template = Template(file.read())
        
        with open(target / "charlotte.config", "w") as file:
            file.write(template.render(name=name, password=password))

        charlotte.articles.initialize(path)
    except FileExistsError:
        print("Please erase the contents of this directory and try again.")

def main():
    if argv[1] == "init":
        name = input("Blog name: ")
        password = input("Password: ")
        init(".", name, password)

if __name__ == "__main__":
    main()