import logging
import sys

import aiohttp_jinja2
import jinja2
from aiohttp import web

from aiohttpdemo_polls.db import pg_context
from aiohttpdemo_polls.middlewares import setup_middlewares
from aiohttpdemo_polls.routes import setup_routes, setup_static_routes
from aiohttpdemo_polls.settings import get_config
from aiohttpdemo_polls.typedefs import config_key


async def init_app(argv=None):

    app = web.Application()

    app[config_key] = get_config(argv)

    # setup Jinja2 template renderer
    aiohttp_jinja2.setup(
        app, loader=jinja2.PackageLoader('aiohttpdemo_polls', 'templates'))

    # create db connection on startup, shutdown on exit
    app.cleanup_ctx.append(pg_context)

    # setup views and routes
    setup_routes(app)
    setup_static_routes(app)
    setup_middlewares(app)

    return app


async def get_app():
    """Used by aiohttp-devtools for local development."""
    import aiohttp_debugtoolbar
    app = await init_app(sys.argv[1:])
    aiohttp_debugtoolbar.setup(app)
    return app


def main(argv):
    logging.basicConfig(level=logging.DEBUG)

    app = init_app(argv)

    config = get_config(argv)
    web.run_app(app,
                host=config['host'],
                port=config['port'])


if __name__ == '__main__':
    main(sys.argv[1:])
