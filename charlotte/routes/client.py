import json

import flask
from flask import render_template, request

from charlotte import app
from charlotte import api

@app.route("/client", methods=["GET"])
def view():
    all_articles = api.get_articles()
    return render_template("client/view.jinja", articles=all_articles)

@app.route("/client/new")
def upload():
    formats = api.get_formats()
    return render_template("client/upload.jinja", formats=formats)

@app.route("/client/update/<article_id>")
def update(article_id):
    article = api.get_article(article_id)
    formats = api.get_formats()
    return render_template("client/update.jinja", article=article, formats=formats)

@app.route("/client", methods=["POST"])
def submit():
    try:
        action = request.form.get("action")
        if action == "delete":
            for value in request.form:
                if value != "action":
                    article_id = value
                    api.delete_article(article_id)
        elif action == "update":
            article_id = request.form.get("article_id")            
            title = request.form.get("title")
            author = request.form.get("author")            
            content = request.form.get("content")            
            article_format = request.form.get("article_format")
            if request.authorization:
                password = request.authorization.password
                api.update_article(article_id, title, author, article_format, content, password)
            else:
                flask.abort(401)
        elif action == "new":
            api.post_article()

        return flask.redirect(flask.url_for("view"), code=303)
    except api.UnauthorizedException as exception:
        flask.abort(401)