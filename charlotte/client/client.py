import requests
from requests.auth import HTTPBasicAuth

class UnauthorizedException(Exception):
    pass

class CharlotteClient:

    def __init__(self, api_path):
        self.api_root = api_path

    def get_url(self, path):
        return self.api_root +  path

    def get_articles(self, password):
        response = requests.get(self.get_url("/articles"), auth=HTTPBasicAuth("", password), timeout=1.0)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise UnauthorizedException()
        else:
            raise Exception()

    def post_article(self, title, author, article_format, content, password):
        response = requests.post(
            self.get_url("/articles"),
            auth=HTTPBasicAuth("", password),
            data={
                "title": title,
                "author": author,
                "format": article_format
            },
            files={"content": content},
            timeout=1.0
        )

    def get_article(self, article_id, password):
        response = requests.get(self.get_url("/articles/%s" % article_id), auth=HTTPBasicAuth("", password), timeout=1.0)
        return response.json()

    def delete_article(self, article_id, password):
        response = requests.delete(self.get_url("/articles/%s" % article_id), auth=HTTPBasicAuth("", password), timeout=1.0)

    def update_article(self, article_id, title, author, article_format, content, password):
        response = requests.patch(
            self.get_url("/articles/%s" % article_id),
            auth=HTTPBasicAuth("", password),
            data={
                "title": title,
                "author": author,
                "format": article_format
            },
            files={"content": content}
        )

    def get_formats(self, password):
        response = requests.get(self.get_url("/formats"), auth=HTTPBasicAuth("", password), timeout=1.0)
        return response.json()