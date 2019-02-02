import sqlite3
import markdown
import slugify

class Article:

    def __init__(self, article_id, title, author, date, slug):
        self.id = article_id
        self.title = title
        self.author = author
        self.date = date
        self.slug = slug

    def get_raw_content(self):
        f = open("articles/{article_id}.md".format(article_id=self.id))
        content = f.read()
        f.close()
        return content

    def get_html(self):
        raw = self.get_raw_content()
        return markdown.markdown(raw)

def initialize_database():
    connection = sqlite3.connect("database.db")
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS articles
            (
                id integer PRIMARY KEY,
                title text NOT NULL,
                author text,
                date date,
                slug text UNIQUE
            );
        """
    )
    connection.close()

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

def get_all_articles():
    connection = sqlite3.connect("database.db")
    cursor = connection.execute("SELECT id, title, author, date, slug FROM articles")
    rows = cursor.fetchall()
    connection.close()

    articles = []
    for row in rows:
        article_id, title, author, date, slug = row
        article = Article(article_id, title, author, date, slug)
        articles.append(article)

    return articles

def get_article(slug):
    connection = sqlite3.connect("database.db")
    query = "SELECT id, title, author, date FROM articles WHERE slug = :slug"
    parameters = { "slug" : slug }
    cursor = connection.execute(query, parameters)
    rows = cursor.fetchall()
    connection.close()

    if len(rows) > 0:
        article_id, title, author, date = rows[0]
        return Article(article_id, title, author, date, slug)
    else:
        return None

def post_article(title, author, content):
    slug = unique_slug_from_title(title)
    connection = sqlite3.connect("database.db")
    query = \
        """
        INSERT INTO articles
            (id, title, author, date, slug)
        VALUES
            (null, :title, :author, date('now'), :slug)
        """
    parameters = \
        { 
            "title": title, "author": author, "slug": slug
        }
    cursor = connection.execute(query, parameters)
    connection.commit()    

    cursor = connection.execute("SELECT last_insert_rowid()")
    rows = cursor.fetchall()
    new_id = rows[0][0]
    f = open("articles/{article_id}.md".format(article_id=new_id), "w")
    f.write(content)
    f.close()
    connection.close()

initialize_database()