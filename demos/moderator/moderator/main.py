import asyncio
import logging

from aiohttp import web

from moderator.consts import PROJ_ROOT
from moderator.handlers import SiteHandler
from moderator.routes import setup_routes
from moderator.utils import load_config, setup_executor


async def init(conf):
    app = web.Application()
    executor = await setup_executor(app, conf)
    handler = SiteHandler(conf, executor, PROJ_ROOT)
    setup_routes(app, handler, PROJ_ROOT)
    return app


async def get_app():
    """Used by aiohttp-devtools for local development."""
    import aiohttp_debugtoolbar
    conf = load_config(PROJ_ROOT / 'config' / 'config.yml')
    app = await init(conf)
    aiohttp_debugtoolbar.setup(app)
    return app


def main():
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    conf = load_config(PROJ_ROOT / 'config' / 'config.yml')
    app = loop.run_until_complete(init(conf))
    host, port = conf['host'], conf['port']
    web.run_app(app, host=host, port=port)


if __name__ == '__main__':
    main()
