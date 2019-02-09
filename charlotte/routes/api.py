from functools import wraps
from flask import request
import flask

from charlotte import app
from charlotte import settings
from charlotte import api

def authenticate(route):
    @wraps(route)
    def authenticated_route(*args, **kwargs):
        if request.authorization is not None:
            password = request.authorization.password
            return route(*args, **kwargs, password=password)
        else:
            flask.abort(401)

    return authenticated_route

@app.errorhandler(api.UnauthorizedException)
def api_unauthorized_handler(exception):
    return "Unauthorized\n", 401

@app.route("/api/articles", methods=["GET"])
@authenticate
def get_articles(password):
    all_articles = api.get_articles(password=password)
    return flask.jsonify(all_articles)

@app.route("/api/articles", methods=["POST"])
@authenticate
def post_article(password):
    title = request.form.get("title", None)
    author = request.form.get("author", None)
    article_format = request.form.get("format", None)
    try:
        content = request.files["content"].read()
    except:
        content = None

    if article_format is None:
        flask.abort(400)
    
    api.post_article(title, author, article_format, content, password=password)

    return ""

@app.route("/api/articles/<article_id>", methods=["GET"])
@authenticate
def get_article(article_id, password):
    article = api.get_article(article_id, password=password)
    return flask.jsonify(article)

@app.route("/api/articles/<article_id>", methods=["DELETE"])
@authenticate
def delete_article(article_id, password):
    api.delete_article(article_id, password=password)
    return ""

@app.route("/api/articles/<article_id>", methods=["PATCH"])
@authenticate
def update_article(article_id, password):
    title = request.form.get("title", None)
    author = request.form.get("author", None)
    article_format = request.form.get("format", None)

    try:
        content = request.files["content"].read()
    except:
        content = None

    if article_format is None:
        flask.abort(400)
    
    api.update_article(article_id, title, author, article_format, content, password=password)

    return ""

@app.route("/api/formats", methods=["GET"])
@authenticate
def get_formats(password):
    formats = api.get_formats(password=password)
    return flask.jsonify(formats)