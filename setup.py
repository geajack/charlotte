import setuptools
from shutil import rmtree

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="charlotte-blog",
    version="1.0.0",
    description="For writing on the web!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/geajack/charlotte",
    packages=setuptools.find_packages(),
    package_data={
        "charlotte": [
            "resources/*",
            "resources/renderers/*",
            "resources/themes/charlotte/*/*"
        ],
        "charlotte.client": [
            "resources/static/*",
            "resources/templates/*"
        ]
    },
    include_package_data=True,
    classifiers=[
    ],
    python_requires='>=3.6',
    install_requires = [
        "Click==7.0",
        "Flask==1.0.2",
        "itsdangerous==1.1.0",
        "Jinja2==2.11.3",
        "Markdown==3.0.1",
        "MarkupSafe==1.1.0",
        "pyyaml>=4.2b1",
        "python-slugify==2.0.1",
        "Werkzeug==0.14.1"
    ],
    entry_points = {
        "console_scripts": [
            "charlotte=charlotte.cli:main"
        ]
    }
)