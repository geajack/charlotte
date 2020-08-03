from pathlib import Path

from flask import Flask

from charlotte.client.routes import ClientController
from charlotte.client.client import CharlotteClient

class CharlotteWebClient(Flask):

    def __init__(self, blog_root):
        super(CharlotteWebClient, self).__init__(
            "Charlotte Web Client",
            template_folder=Path(__file__).parent / "resources/templates",
            static_folder=Path(__file__).parent / "resources/static"
        )
        self.client = CharlotteClient(blog_root + "/api")
        self.controller = ClientController(blog_root, self.client)
        ClientController.route_table.add_to_app(self.controller, self)