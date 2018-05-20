from pathlib import Path

import aiopg.sa
from aiohttp import web
import aiohttp_jinja2
import jinja2

from .routes import init_routes
from .utils import init_config


path = Path(__file__).parent


def init_jinja2(app: web.Application) -> None:
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(str(path / 'templates'))
    )


async def init_database(app: web.Application) -> None:
    config = app['config']['postgres']

    engine = await aiopg.sa.create_engine(**config)
    app['db'] = engine


async def close_database(app: web.Application) -> None:
    app['db'].close()
    await app['db'].wait_closed()


def init_app() -> web.Application:
    app = web.Application()

    init_jinja2(app)
    init_config(app)
    init_routes(app)

    app.on_startup.append(init_database)
    app.on_cleanup.append(close_database)

    return app
