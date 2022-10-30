import logging

import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiohttp_security import SessionIdentityPolicy
from aiohttp_security import authorized_userid
from aiohttp_security import setup as setup_security
from aiohttp_session import setup as setup_session
from aiohttp_session.redis_storage import RedisStorage
from redis import asyncio as aioredis
from aiohttpdemo_blog.db_auth import DBAuthorizationPolicy
from aiohttpdemo_blog.db import init_db
from aiohttpdemo_blog.routes import setup_routes
from aiohttpdemo_blog.settings import load_config, PACKAGE_NAME


log = logging.getLogger(__name__)


async def setup_redis(app):

    redis_host = app["config"]["redis"]["REDIS_HOST"]
    redis_port = app["config"]["redis"]["REDIS_PORT"]

    redis = await aioredis.from_url(f"redis://{redis_host}:{redis_port}")
    app["redis"] = redis
    return redis


async def current_user_ctx_processor(request):
    username = await authorized_userid(request)
    is_anonymous = not bool(username)
    return {'current_user': {'is_anonymous': is_anonymous}}


async def init_app(config):

    app = web.Application()

    app['config'] = config

    setup_routes(app)

    db_pool = await init_db(app)

    redis = await setup_redis(app)
    setup_session(app, RedisStorage(redis))

    # needs to be after session setup because of `current_user_ctx_processor`
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader(PACKAGE_NAME),
        context_processors=[current_user_ctx_processor],
    )

    setup_security(
        app,
        SessionIdentityPolicy(),
        DBAuthorizationPolicy(db_pool)
    )

    log.debug(app['config'])

    return app


async def get_app():
    """Used by aiohttp-devtools for local development."""
    import argparse
    import aiohttp_debugtoolbar
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Provide path to config file")
    args = parser.parse_args()

    app = await init_app(args.config)
    aiohttp_debugtoolbar.setup(app)
    return app


def main(configpath):
    config = load_config(configpath)
    logging.basicConfig(level=logging.DEBUG)
    app = init_app(config)
    web.run_app(app)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Provide path to config file")
    args = parser.parse_args()

    if args.config:
        main(args.config)
    else:
        parser.print_help()
