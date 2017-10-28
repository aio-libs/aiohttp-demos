import asyncio
import logging
import pathlib

import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiohttp_security import setup as setup_security
from aiohttp_security import CookiesIdentityPolicy

from motortwit.routes import setup_routes
from motortwit.security import AuthorizationPolicy
from motortwit.utils import (format_datetime, init_mongo, load_config,
                             robo_avatar_url)
from motortwit.views import SiteHandler


PROJ_ROOT = pathlib.Path(__file__).parent.parent
TEMPLATES_ROOT = pathlib.Path(__file__).parent / 'templates'


async def setup_mongo(app, conf, loop):
    mongo = await init_mongo(conf['mongo'], loop)

    async def close_mongo(app):
        mongo.client.close()

    app.on_cleanup.append(close_mongo)
    return mongo


def setup_jinja(app):
    jinja_env = aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader(str(TEMPLATES_ROOT)))

    jinja_env.filters['datetimeformat'] = format_datetime
    jinja_env.filters['robo_avatar_url'] = robo_avatar_url


async def init(loop):
    conf = load_config(PROJ_ROOT / 'config' / 'config.yml')

    app = web.Application(loop=loop)
    mongo = await setup_mongo(app, conf, loop)

    setup_jinja(app)
    setup_security(app, CookiesIdentityPolicy(), AuthorizationPolicy(mongo))

    # setup views and routes
    handler = SiteHandler(mongo)
    setup_routes(app, handler, PROJ_ROOT)
    host, port = conf['host'], conf['port']
    return app, host, port


def main():
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    app, host, port = loop.run_until_complete(init(loop))
    web.run_app(app, host=host, port=port)


if __name__ == '__main__':
    main()
