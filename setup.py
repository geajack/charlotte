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
    packages=["charlotte"],
    classifiers=[
    ],
    python_requires='>=3.6',
)

rmtree("charlotte_blog.egg-info")
rmtree("build")