import asyncio
import logging
import pathlib

import aiohttp_jinja2
import jinja2
from aiohttp import web
from redis.asyncio import Redis

from shortify.routes import setup_routes
from shortify.utils import init_redis, load_config
from shortify.views import SiteHandler


PROJ_ROOT = pathlib.Path(__file__).parent.parent
TEMPLATES_ROOT = pathlib.Path(__file__).parent / 'templates'

# Define AppKey for Redis
REDIS_KEY = web.AppKey("REDIS_KEY", Redis)


async def setup_redis(app, conf):
    redis = await init_redis(conf["redis"])
    app[REDIS_KEY] = redis
    return redis


def setup_jinja(app):
    loader = jinja2.FileSystemLoader(str(TEMPLATES_ROOT))
    jinja_env = aiohttp_jinja2.setup(app, loader=loader)
    return jinja_env


async def init():
    conf = load_config(PROJ_ROOT / "config" / "config.yml")

    app = web.Application()
    redis = await setup_redis(app, conf)
    setup_jinja(app)

    handler = SiteHandler(redis, conf)

    setup_routes(app, handler, PROJ_ROOT)
    host, port = conf['host'], conf['port']
    return app, host, port


async def get_app():
    """Used by aiohttp-devtools for local development."""
    import aiohttp_debugtoolbar
    app, _, _ = await init()
    aiohttp_debugtoolbar.setup(app)
    return app


def main():
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    app, host, port = loop.run_until_complete(init())
    web.run_app(app, host=host, port=port)


if __name__ == '__main__':
    main()
