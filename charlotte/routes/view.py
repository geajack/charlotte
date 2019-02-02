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
    head = ""
    renderers = set([article.renderer for article in all_articles])
    for renderer in renderers:
        head += renderer.head()
        head += "\n"
    return render_template("index.html", articles=all_articles, head=Markup(head))

@app.route("/articles/<slug>")
def article(slug=None):
    article = articles.get_article(slug)
    if article is not None:
        return render_template(
            "article.html",
            title=article.title,
            author=article.author,
            date=article.date,
            content=Markup(article.get_content_html()),
            head=Markup(article.get_head_html())
        )
    else:
        flask.abort(404)

@app.route("/upload")
def upload():
    return render_template("upload.html")