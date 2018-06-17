import asyncio
import logging

from aiohttp import web

from moderator.consts import PROJ_ROOT
from moderator.handlers import SiteHandler
from moderator.routes import setup_routes
from moderator.utils import load_config, setup_executor


async def init(loop, conf):
    app = web.Application(loop=loop)
    executor = await setup_executor(app, conf)
    handler = SiteHandler(conf, executor, PROJ_ROOT)
    setup_routes(app, handler, PROJ_ROOT)
    return app


def main():
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    conf = load_config(PROJ_ROOT / 'config' / 'config.yml')
    app = loop.run_until_complete(init(loop, conf))
    host, port = conf['host'], conf['port']
    web.run_app(app, host=host, port=port)


if __name__ == '__main__':
    main()
