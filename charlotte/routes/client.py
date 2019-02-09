import json

from functools import wraps
import flask
from flask import render_template, request

from charlotte import app
from charlotte import api

def requires_login(route):
    @wraps(route)
    def authenticated_route(*args, **kwargs):
        password = request.cookies.get("password")
        print(password)
        return route(*args, **kwargs, password=password)

    return authenticated_route

@app.route("/client", methods=["GET"])
@requires_login
def view(password=None):
    all_articles = api.get_articles(password=password)
    return render_template("client/view.jinja", articles=all_articles)

@app.route("/client/new")
@requires_login
def upload(password=None):
    formats = api.get_formats(password=password)
    return render_template("client/upload.jinja", formats=formats)

@app.route("/client/update/<article_id>")
@requires_login
def update(article_id, password=None):
    article = api.get_article(article_id, password=password)
    formats = api.get_formats(password=password)
    return render_template("client/update.jinja", article=article, formats=formats)

@app.route("/client", methods=["POST"])
@requires_login
def submit(password=None):
    try:
        action = request.form.get("action")

        if action == "delete":
            for value in request.form:
                if value != "action":
                    article_id = value
                    api.delete_article(article_id, password=password)
        elif action == "update":
            article_id = request.form.get("article_id")            
            title = request.form.get("title")
            author = request.form.get("author")            
            article_format = request.form.get("format")

            if article_format is None:
                flask.abort(400)

            try:
                content = request.files["content"].read()
            except:
                content = None
            api.update_article(article_id, title, author, article_format, content, password=password)
        elif action == "new":
            title = request.form.get("title")
            author = request.form.get("author")            
            article_format = request.form.get("format")

            if article_format is None:
                flask.abort(400)

            try:
                content = request.files["content"].read()
            except:
                content = None
            api.post_article(title, author, article_format, content, password=password)

        return flask.redirect(flask.url_for("view"), code=303)
    except api.UnauthorizedException:
        flask.abort(401)