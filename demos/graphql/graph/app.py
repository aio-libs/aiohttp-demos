from pathlib import Path

import aiopg.sa
from aiohttp import web
import aiohttp_jinja2
import jinja2

from graph.routes import init_routes
from graph.utils import init_config
from graph.api.dataloaders import UserLoader


path = Path(__file__).parent


def init_jinja2(app: web.Application) -> None:
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(str(path / 'templates'))
    )


async def init_database(app: web.Application) -> None:
    '''
    This is signal for success creating connection with database
    '''
    config = app['config']['postgres']

    engine = await aiopg.sa.create_engine(**config)
    app['db'] = engine


async def close_database(app: web.Application) -> None:
    '''
    This is signal for success closing connection with database before shutdown
    '''
    app['db'].close()
    await app['db'].wait_closed()


async def init_graph_loaders(app: web.Application) -> None:
    '''
    The function initialize data loaders for `graphene`. U should initialize it
    after initialize a database.
    '''
    engine = app['db']

    class Loaders:
        users = UserLoader(engine)

    app['loaders'] = Loaders()


def init_app() -> web.Application:
    app = web.Application()

    init_jinja2(app)
    init_config(app)
    init_routes(app)

    app.on_startup.extend([init_database, init_graph_loaders])
    app.on_cleanup.append(close_database)

    return app
