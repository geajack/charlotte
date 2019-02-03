from flask import request
import flask

from charlotte import app
from charlotte import settings
from charlotte import articles

@app.route("/api/articles", methods=["GET"])
def get_articles():
    return []

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
        articles.post_article(title, author, article_format, content)

    return ""

@app.route("/api/articles/<article_id>", methods=["GET"])
def get_article(article_id):
    article = articles.get_article_by_id(article_id)
    if article is not None:
        return flask.jsonify(article.as_api_entity())
    else:
        flask.abort(404)

@app.route("/api/articles/<article_id>", methods=["DELETE"])
def delete_article(article_id):
    pass

@app.route("/api/articles/<article_id>", methods=["PATCH"])
def update_article(article_id):
    pass

@app.route("/api/formats", methods=["GET"])
def get_formats():
    pass