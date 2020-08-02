from functools import wraps

import flask
from flask import Flask
from flask import render_template, request

import charlotte.client
from charlotte.client import app

def blog_url(path):
    return "http://localhost:8000" + path

@app.context_processor
def inject():
    return {
        "blog_url": blog_url
    }

def requires_login(route):
    @wraps(route)
    def authenticated_route(*args, **kwargs):
        try:
            password = request.cookies.get("password")
            return route(*args, **kwargs, password=password)
        except charlotte.client.UnauthorizedException:
            return flask.redirect(flask.url_for("login"))

    return authenticated_route

@app.route("/login", methods=["GET"])
def login():
    return render_template("login.jinja", incorrect=False)

@app.route("/login", methods=["POST"])
def submit_login():
    password = request.form.get("password")
    try:
        charlotte.client.get_articles(password=password)
    except charlotte.client.UnauthorizedException:
        return render_template("login.jinja", incorrect=True)

    response = flask.redirect(flask.url_for("view"), code=303)        
    response.set_cookie("password", value=password)
    return response

@app.route("/", methods=["GET"])
@requires_login
def view(password=None):
    all_articles = charlotte.client.get_articles(password=password)
    return render_template("view.jinja", articles=all_articles)

@app.route("/new")
@requires_login
def upload(password=None):
    formats = charlotte.client.get_formats(password=password)
    return render_template("upload.jinja", formats=formats)

@app.route("/update/<article_id>")
@requires_login
def update(article_id, password=None):
    article = charlotte.client.get_article(article_id, password=password)
    formats = charlotte.client.get_formats(password=password)
    return render_template("update.jinja", article=article, formats=formats)

@app.route("/", methods=["POST"])
@requires_login
def submit(password=None):
    try:
        action = request.form.get("action")

        if action == "delete":
            for value in request.form:
                if value != "action":
                    article_id = value
                    charlotte.client.delete_article(article_id, password=password)
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
            charlotte.client.update_article(article_id, title, author, article_format, content, password=password)
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
            charlotte.client.post_article(title, author, article_format, content, password=password)

        return flask.redirect(flask.url_for("view"), code=303)
    except charlotte.client.UnauthorizedException:
        flask.abort(401)