import os
import sqlite3
from datetime import datetime

import slugify

from charlotte import app
from charlotte import settings
from charlotte import renderers
from charlotte import api

class Article:

    def __init__(self, article_id, title, author, article_format, date, slug):
        self.id = article_id
        self.title = title
        self.author = author
        self.article_format = article_format
        self.date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        self.slug = slug
        self.renderer = renderers.get_renderer(article_format)

    def display_title(self):
        if self.title == "":
            return self.date.strftime("%d %B %Y")
        else:
            return self.title

    def get_raw_content(self):
        f = open("articles/content/{slug}".format(slug=self.slug))
        content = f.read()
        f.close()
        return content

    def get_content_html(self):
        raw = self.get_raw_content()
        return self.renderer.render(raw)

    def get_head_html(self):
        if hasattr(self.renderer, "head"):
            return self.renderer.head()

    def get_file_path(self):
        return "articles/content/{slug}".format(slug=self.slug)

    def as_api_entity(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "format": self.article_format,
            "date": self.date,
            "slug": self.slug,
            "content": self.get_raw_content()
        }

    def as_api_header(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "format": self.article_format,
            "date": self.date,
            "slug": self.slug
        }

def initialize():
    try:
        with sqlite3.connect("articles/database.db") as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS articles
                    (
                        id integer PRIMARY KEY,
                        title text NOT NULL,
                        author text,
                        format text,
                        date datetime,
                        slug text UNIQUE
                    );
                """
            )
        charlotte_root = settings.get_charlotte_root()
        (charlotte_root / "articles" / "content").mkdir(exist_ok=True)
    except:
        app.logger.error("Could not initialize database")

def slug_from_title(title):
    if title == "":
        return "untitled"
    else:
        return slugify.slugify(title)

def unique_slug_from_title(title):
    slug = slug_from_title(title)
    
    connection = sqlite3.connect("articles/database.db")
    cursor = connection.execute("SELECT slug FROM articles")
    rows = cursor.fetchall()
    connection.close()

    slugs = [row[0] for row in rows]
    n = 2
    unique_slug = slug
    while unique_slug in slugs:
        unique_slug = slug + "-" + str(n)
        n += 1
    return unique_slug

def updated_unique_slug(article_id, title):
    slug = slug_from_title(title)
    
    connection = sqlite3.connect("articles/database.db")
    cursor = connection.execute("SELECT id, slug FROM articles")
    rows = cursor.fetchall()
    connection.close()

    slugs = [row[1] for row in rows if row[0] != article_id]
    n = 2
    unique_slug = slug
    while unique_slug in slugs:
        unique_slug = slug + "-" + str(n)
        n += 1
    return unique_slug

def how_many():
    connection = sqlite3.connect("articles/database.db")
    cursor = connection.execute("SELECT COUNT(*) FROM articles")
    row = cursor.fetchone()
    connection.close()
    number = row[0]
    return number

def get_all():
    connection = sqlite3.connect("articles/database.db")
    query = """
        SELECT id, title, author, format, date, slug FROM articles
        ORDER BY date DESC
    """
    cursor = connection.execute(query)
    rows = cursor.fetchall()
    connection.close()

    articles = []
    for row in rows:
        article_id, title, author, article_format, date, slug = row
        article = Article(article_id, title, author, article_format, date, slug)
        articles.append(article)

    return articles

def get_latest_articles(skip, number):
    connection = sqlite3.connect("articles/database.db")
    query = """
        SELECT id, title, author, format, date, slug FROM articles
        ORDER BY date DESC
        LIMIT :skip, :number
    """
    parameters = {
        "skip": skip,
        "number": number
    }
    cursor = connection.execute(query, parameters)
    rows = cursor.fetchall()
    connection.close()

    articles = []
    for row in rows:
        article_id, title, author, article_format, date, slug = row
        article = Article(article_id, title, author, article_format, date, slug)
        articles.append(article)

    return articles

def get_article_by_id(article_id):
    connection = sqlite3.connect("articles/database.db")
    query = "SELECT id, title, author, format, date, slug FROM articles WHERE id = :id"
    parameters = { "id" : article_id }
    cursor = connection.execute(query, parameters)
    row = cursor.fetchone()
    connection.close()

    try:
        article_id, title, author, article_format, date, slug = row
        return Article(article_id, title, author, article_format, date, slug)
    except:
        return None

def get_article_by_slug(slug):
    connection = sqlite3.connect("articles/database.db")
    query = "SELECT id, title, author, format, date FROM articles WHERE slug = :slug"
    parameters = { "slug" : slug }
    cursor = connection.execute(query, parameters)
    rows = cursor.fetchall()
    connection.close()

    if len(rows) > 0:
        article_id, title, author, article_format, date = rows[0]
        return Article(article_id, title, author, article_format, date, slug)
    else:
        return None

def post_article(title, author, article_format, content):
    slug = unique_slug_from_title(title)
    connection = sqlite3.connect("articles/database.db")
    query = \
        """
        INSERT INTO articles
            (id, title, author, format, date, slug)
        VALUES
            (null, :title, :author, :article_format, datetime('now'), :slug)
        """
    parameters = \
        { 
            "title": title, "author": author, "slug": slug, "article_format": article_format
        }
    connection.execute(query, parameters)
    connection.commit()    

    cursor = connection.execute("SELECT last_insert_rowid()")
    rows = cursor.fetchall()
    new_id = rows[0][0]
    f = open("articles/content/{slug}".format(slug=slug), "wb")
    f.write(content)
    f.close()
    connection.close()

def delete_article(article_id):
    try:
        article = get_article_by_id(article_id)
        article_file = article.get_file_path()

        connection = sqlite3.connect("articles/database.db")
        query = "DELETE FROM articles WHERE id = :id"
        parameters = { "id": article_id }
        connection.execute(query, parameters)
        connection.commit()
        
        os.remove(article_file)
    except Exception as exception:
        app.logger.error("Could not delete article {article_id}: {exception}".format(article_id=article_id, exception=exception))
    finally:
        connection.close()

def update_article(article_id, title=None, author=None, format=None, content=None):
    article = get_article_by_id(article_id)

    if title is not None:
        slug = updated_unique_slug(article_id, title)
        old_file = article.get_file_path()
        os.rename(old_file, "articles/content/{slug}".format(slug=slug))
    else:
        slug = article.slug

    if content is not None:
        f = open("articles/content/{slug}".format(slug=slug), "wb")
        f.write(content)
        f.close()

    try:
        connection = sqlite3.connect("articles/database.db")    
        query = """
            UPDATE articles
            SET
                title = COALESCE(:title, title),
                author = COALESCE(:author, author),
                format = COALESCE(:format, format),
                slug = COALESCE(:slug, slug)
            WHERE
                id = :article_id
            """
        parameters = {
            "article_id": article_id,
            "title": title,
            "author": author,
            "format": format,
            "slug": slug,
            "content": content
        }
        connection.execute(query, parameters)
        connection.commit()
    finally:
        connection.close()
    

initialize()