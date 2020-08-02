from pathlib import Path

from flask import Flask

from charlotte.client.routes import route_table

app = Flask(
    "Charlotte Web Client",
    template_folder=Path(__file__).parent / "resources/templates",
    static_folder=Path(__file__).parent / "resources/static"
)
route_table.add_to_app(app)

application = app