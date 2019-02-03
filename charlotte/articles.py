import sqlite3
import slugify

from charlotte import settings
from charlotte import renderers

class Article:

    def __init__(self, article_id, title, author, article_format, date, slug):
        self.id = article_id
        self.title = title
        self.author = author
        self.article_format = article_format
        self.date = date
        self.slug = slug
        self.renderer = renderers.get_renderer(article_format)

    def get_raw_content(self):
        f = open("articles/{slug}.md".format(slug=self.slug))
        content = f.read()
        f.close()
        return content

    def get_content_html(self):
        raw = self.get_raw_content()
        return self.renderer.render(raw)

    def get_head_html(self):
        if hasattr(self.renderer, "head"):
            return self.renderer.head()

    def as_api_entity(self):
        dictionary = {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "date": self.date,
            "slug": self.slug,
            "format": self.article_format,
            "content": self.get_raw_content()
        }
        return dictionary

def initialize():
    connection = sqlite3.connect("database.db")
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
    connection.close()

    charlotte_root = settings.get_charlotte_root()
    (charlotte_root / "articles").mkdir(exist_ok=True)

def slug_from_title(title):
    return slugify.slugify(title)

def unique_slug_from_title(title):
    slug = slug_from_title(title)
    
    connection = sqlite3.connect("database.db")
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

def how_many():
    connection = sqlite3.connect("database.db")
    cursor = connection.execute("SELECT COUNT(*) FROM articles")
    row = cursor.fetchone()
    connection.close()
    number = row[0]
    return number


def get_latest_articles(skip, number):
    connection = sqlite3.connect("database.db")
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
    connection = sqlite3.connect("database.db")
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
    connection = sqlite3.connect("database.db")
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
    connection = sqlite3.connect("database.db")
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
    cursor = connection.execute(query, parameters)
    connection.commit()    

    cursor = connection.execute("SELECT last_insert_rowid()")
    rows = cursor.fetchall()
    new_id = rows[0][0]
    f = open("articles/{slug}.md".format(slug=slug), "wb")
    f.write(content)
    f.close()
    connection.close()

initialize()