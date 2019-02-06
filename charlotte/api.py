from charlotte import app
from charlotte import articles
from charlotte import settings

class CharlotteAPIException(Exception):
    pass

class UnauthorizedException(CharlotteAPIException):
    pass

def get_articles():
    all_articles = articles.get_all()
    headers = [article.as_api_header() for article in all_articles]
    return headers

def post_article(title, author, article_format, content, password):
    authenticated = settings.is_password_correct(password)
    if authenticated:
        articles.post_article(title, author, article_format, content)
    else:
        raise UnauthorizedException()

def get_article(article_id):
    article = articles.get_article_by_id(article_id)
    if article is not None:
        return article.as_api_entity()
    else:
        raise CharlotteAPIException()

def delete_article(article_id, password):    
    authenticated = settings.is_password_correct(password)
    if authenticated:
        articles.delete_article(article_id)
    else:
        raise UnauthorizedException()

def update_article(article_id, title, author, article_format, content, password):
    authenticated = settings.is_password_correct(password)
    if authenticated:
        articles.update_article(article_id, title=title, author=author, format=article_format, content=content)
    else:
        raise UnauthorizedException()

def get_formats():
    formats = settings.get_formats()
    return [format_object.as_api_entity() for format_object in formats]