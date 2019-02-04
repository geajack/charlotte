import json

import flask
from flask import render_template, request

from charlotte import app
from charlotte.routes import api

@app.route("/client", methods=["GET"])
def view():
    all_articles = api.get_articles().get_json()
    return render_template("client/view.jinja", articles=all_articles)

@app.route("/client/new")
def upload():
    formats = api.get_formats().get_json()
    return render_template("client/upload.jinja", formats=formats)

@app.route("/client/update/<article_id>")
def update(article_id):
    article = api.get_article(article_id).get_json()
    formats = api.get_formats().get_json()
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
            api.update_article(article_id)
        elif action == "new":
            api.post_article()

        return flask.redirect(flask.url_for("view"), code=303)
    except Exception as exception:
        app.logger.error("Could not POST action to web client: {exception}".format(exception=exception))