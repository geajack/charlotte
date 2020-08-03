from functools import wraps

import flask
from flask import Flask
from flask import render_template, request

from charlotte.RouteTable import RouteTable
from charlotte.client.client import UnauthorizedException

def requires_login(route):
    @wraps(route)
    def authenticated_route(*args, **kwargs):
        try:
            password = request.cookies.get("password")
            return route(*args, **kwargs, password=password)
        except UnauthorizedException:
            return flask.redirect(flask.url_for("login"))

    return authenticated_route

class ClientController:

    route_table = RouteTable()

    def __init__(self, blog_root, client):
        self.blog_root = blog_root
        self.client = client

    def get_blog_url(self, path):
        return self.blog_root + path

    @route_table.context_processor
    def inject(self):
        return {
            "blog_url": self.get_blog_url
        }

    @route_table.route("/login", methods=["GET"])
    def login(self):
        return render_template("login.jinja", incorrect=False)

    @route_table.route("/login", methods=["POST"])
    def submit_login(self):
        password = request.form.get("password")
        try:
            self.client.get_articles(password=password)
        except self.client.UnauthorizedException:
            return render_template("login.jinja", incorrect=True)

        response = flask.redirect(flask.url_for("view"), code=303)        
        response.set_cookie("password", value=password)
        return response

    @route_table.route("/", methods=["GET"])
    @requires_login
    def view(self, password=None):
        all_articles = self.client.get_articles(password=password)
        return render_template("view.jinja", articles=all_articles)

    @route_table.route("/new")
    @requires_login
    def upload(self, password=None):
        formats = self.client.get_formats(password=password)
        return render_template("upload.jinja", formats=formats)

    @route_table.route("/update/<article_id>")
    @requires_login
    def update(self, article_id, password=None):
        article = self.client.get_article(article_id, password=password)
        formats = self.client.get_formats(password=password)
        return render_template("update.jinja", article=article, formats=formats)

    @route_table.route("/", methods=["POST"])
    @requires_login
    def submit(self, password=None):
        try:
            action = request.form.get("action")

            if action == "delete":
                for value in request.form:
                    if value != "action":
                        article_id = value
                        self.client.delete_article(article_id, password=password)
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
                self.client.update_article(article_id, title, author, article_format, content, password=password)
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
                self.client.post_article(title, author, article_format, content, password=password)

            return flask.redirect(flask.url_for("view"), code=303)
        except UnauthorizedException:
            flask.abort(401)