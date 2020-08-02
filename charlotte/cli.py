from pathlib import Path
from shutil import copytree, copy
from sys import argv

import charlotte.articles

def init(path):
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
    copy(
        src=resources_directory / "charlotte.config",
        dst=target
    )

    charlotte.articles.initialize(path)

def main():
    if argv[1] == "init":
        init(".")