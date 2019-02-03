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
@app.route("/<page>")
def index(page="1"):
    page = int(page)
    number = 10
    skip = (page - 1) * number
    visible_articles = articles.get_latest_articles(skip, number)

    number_of_articles = articles.how_many()
    number_of_pages = int(number_of_articles / number) + 1
    previous_page = None
    next_page = None
    if page < number_of_pages:
        next_page = page + 1
    if page > 1:
        previous_page = page - 1

    head = ""
    renderers = set([article.renderer for article in visible_articles])
    for renderer in renderers:
        head += renderer.head()
        head += "\n"

    return render_template(
        "blog/index.jinja",
        articles=visible_articles,
        renderer_head=Markup(head),
        next_page=next_page,
        previous_page=previous_page
    )

@app.route("/articles/<slug>")
def article(slug=None):
    article = articles.get_article(slug)
    if article is not None:
        return render_template(
            "blog/article.jinja",
            title=article.title,
            author=article.author,
            date=article.date,
            content=Markup(article.get_content_html()),
            renderer_head=Markup(article.get_head_html())
        )
    else:
        flask.abort(404)

@app.route("/upload")
def upload():
    return render_template("client/upload.jinja")