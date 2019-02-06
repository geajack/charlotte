from flask import request
import flask

from charlotte import app
from charlotte import settings
from charlotte import api

@app.errorhandler(api.UnauthorizedException)
def api_unauthorized_handler(exception):
    flask.abort(401)

@app.route("/api/articles", methods=["GET"])
def get_articles():
    all_articles = api.get_articles()
    return flask.jsonify(all_articles)

@app.route("/api/articles", methods=["POST"])
def post_article():
    title = request.form["title"]
    author = request.form["author"]
    article_format = request.form["format"]
    try:
        content = request.files["content"].read()
    except:
        flask.abort(400)
    else:
        api.post_article(title, author, article_format, content)

    return ""

@app.route("/api/articles/<article_id>", methods=["GET"])
def get_article(article_id):
    article = api.get_article(article_id)
    return flask.jsonify(article)

@app.route("/api/articles/<article_id>", methods=["DELETE"])
def delete_article(article_id):
    if request.authorization is not None:
        api.delete_article(article_id, request.authorization.password)
        return ""
    else:
        flask.abort(401)

@app.route("/api/articles/<article_id>", methods=["PATCH"])
def update_article(article_id):
    title = request.form.get("title", None)
    author = request.form.get("author", None)
    article_format = request.form.get("format", None)

    try:
        content = request.files["content"].read()
    except:
        content = None
    
    api.update_article(article_id, title, author, article_format, content)

    return ""

@app.route("/api/formats", methods=["GET"])
def get_formats():
    formats = api.get_formats()
    return flask.jsonify(formats)