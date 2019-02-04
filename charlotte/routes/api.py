from flask import request
import flask

from charlotte import app
from charlotte import settings
from charlotte import articles

@app.route("/api/articles", methods=["GET"])
def get_articles():
    all_articles = articles.get_all()
    api_entities = [article.as_api_header_entity() for article in all_articles]
    return flask.jsonify(api_entities)

@app.route("/api/articles", methods=["POST"])
def post_article():
    try:
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
    except Exception as exception:
        app.logger.error("Charlotte API suffered an error while processing POST /articles: {exception}".format(exception=exception))

@app.route("/api/articles/<article_id>", methods=["GET"])
def get_article(article_id):
    article = articles.get_article_by_id(article_id)
    if article is not None:
        return flask.jsonify(article.as_api_entity())
    else:
        flask.abort(404)

@app.route("/api/articles/<article_id>", methods=["DELETE"])
def delete_article(article_id):    
    articles.delete_article(article_id)
    return ""

@app.route("/api/articles/<article_id>", methods=["PATCH"])
def update_article(article_id):
    title = request.form.get("title", None)
    author = request.form.get("author", None)
    article_format = request.form.get("format", None)

    try:
        content = request.files["content"].read()
    except:
        content = None
    
    articles.update_article(article_id, title=title, author=author, format=article_format, content=content)

    return ""

@app.route("/api/formats", methods=["GET"])
def get_formats():
    formats = settings.get_formats()
    api_entities = [format_object.as_api_entity() for format_object in formats]
    return flask.jsonify(api_entities)