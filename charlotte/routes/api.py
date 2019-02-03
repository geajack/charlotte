from flask import request
import flask

from charlotte import app
from charlotte import settings
from charlotte import articles

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