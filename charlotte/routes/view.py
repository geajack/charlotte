import codecs

from flask import render_template, Markup
import flask
from jinja2 import BaseLoader
from jinja2.parser import Parser
from jinja2.exceptions import TemplateNotFound

from charlotte import app
from charlotte import articles
from charlotte import settings

class CharlotteTemplateLoader(BaseLoader):

    def __init__(self):
        pass

    def get_source(self, environment, name):
        theme_folder = settings.get_theme_directory()
        if theme_folder is None:
            raise TemplateNotFound(name)

        template_path = theme_folder / "templates" / name
        print(template_path)
        try:
            with open(template_path) as f:
                return f.read(), str(template_path), self.use_cache.__get__(self, CharlotteTemplateLoader)
        except FileNotFoundError:
            raise TemplateNotFound(name)

    def use_cache(self, path):
        return False

app.jinja_loader = CharlotteTemplateLoader()

@app.context_processor
def inject():
    return {
        "blog_name": settings.get_blog_name()
    }

@app.route("/")
@app.route("/<page>")
def index(page="1"):
    try:
        page = int(page)
    except:
        flask.abort(404)

    articles_per_page = 10
    number_of_articles = articles.how_many()
    number_of_pages = int(number_of_articles / articles_per_page) + 1

    if page < 1 or page > number_of_pages:
        return flask.redirect("/")
    else:
        skip = (page - 1) * articles_per_page
        visible_articles = articles.get_latest_articles(skip, articles_per_page)
        
        previous_page = None
        next_page = None
        if page < number_of_pages:
            next_page = page + 1
        if page > 1:
            previous_page = page - 1

        head = ""
        renderers = set([article.renderer for article in visible_articles])
        for renderer in renderers:
            if hasattr(renderer, "head"):
                head += renderer.head()
                head += "\n"

        return render_template(
            "index.jinja",
            articles=visible_articles,
            renderer_head=Markup(head),
            next_page=next_page,
            previous_page=previous_page
        )

@app.route("/articles/<slug>")
def article(slug=None):
    article = articles.get_article_by_slug(slug)
    if article is not None:
        return render_template(
            "article.jinja",
            title=article.display_title(),
            author=article.author,
            date=article.date,
            format=article.article_format,
            content=Markup(article.get_content_html()),
            renderer_head=Markup(article.get_head_html())
        )
    else:
        flask.abort(404)

@app.route("/theme/<path:path>")
def theme(path):
    theme_directory = settings.get_theme_directory()
    if theme_directory is not None:
        return flask.send_from_directory(theme_directory, path)
    else:
        return ""
