from pathlib import Path

from aiohttp import web
import aiohttp_jinja2
import jinja2

from .routes import init_routes


path = Path(__file__).parent


def init_jinja2(app: web.Application) -> None:
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(str(path / 'templates'))
    )


def init_app() -> web.Application:
    app = web.Application()

    init_jinja2(app)
    init_routes(app)

    return app
