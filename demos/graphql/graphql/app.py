from pathlib import Path

from aiohttp import web
import aiohttp_jinja2
import jinja2

from .routes import routes
from .main.views import index  # noqa
from .api.views import graph_handler  # noqa


path = Path(__file__).parent


def init_jinja2(app: web.Application) -> None:
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(str(path / 'templates'))
    )


def init_app() -> web.Application:
    app = web.Application()
    app.add_routes(routes)

    init_jinja2(app)

    return app
