from pathlib import Path

from flask import Flask
import requests
from requests.auth import HTTPBasicAuth

app = Flask(
    "Charlotte Web Client",
    template_folder=Path(__file__).parent / "resources/templates",
    static_folder=Path(__file__).parent / "resources/static"
)
application = app

class UnauthorizedException(Exception):
    pass

def get_url(path):
    return "http://localhost:8000" + "/api/" +  path

def get_articles(password):
    response = requests.get(get_url("articles"), auth=HTTPBasicAuth("", password))
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        raise UnauthorizedException()
    else:
        print(get_url("articles"))
        print(response.status_code)

def post_article(title, author, article_format, content, password):
    response = requests.post(
        get_url("articles"),
        auth=HTTPBasicAuth("", password),
        data={
            "title": title,
            "author": author,
            "format": article_format
        },
        files={"content": content}
    )

def get_article(article_id, password):
    response = requests.get(get_url("articles/%s" % article_id), auth=HTTPBasicAuth("", password))
    return response.json()

def delete_article(article_id, password):
    response = requests.delete(get_url("articles/%s" % article_id), auth=HTTPBasicAuth("", password))

def update_article(article_id, title, author, article_format, content, password):
    response = requests.patch(
        get_url("articles/%s" % article_id),
        auth=HTTPBasicAuth("", password),
        data={
            "title": title,
            "author": author,
            "format": article_format
        },
        files={"content": content}
    )

def get_formats(password):
    response = requests.get(get_url("formats"), auth=HTTPBasicAuth("", password))
    return response.json()

import charlotte.client.routes