from flask import render_template, Markup
import flask

from charlotte import app
from charlotte import articles
from charlotte import settings

@app.context_processor
def inject():
    return {
        "blog_name": settings.get_blog_name()
    }

@app.route("/")
def index():
    all_articles = articles.get_all_articles()
    return render_template("index.html", articles=all_articles)

@app.route("/articles/<slug>")
def article(slug=None):
    article = articles.get_article(slug)
    if article is not None:
        return render_template(
            "article.html",
            title=article.title,
            author=article.author,
            date=article.date,
            content=Markup(article.get_html())
        )
    else:
        flask.abort(404)