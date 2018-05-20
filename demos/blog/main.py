import logging

import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiohttp_security import SessionIdentityPolicy
from aiohttp_security import setup as setup_security
from aiohttp_session import setup as setup_session
from aiohttp_session.redis_storage import RedisStorage
from aioredis import create_pool

from config import user_config
from db import setup_db
from db_auth import DBAuthorizationPolicy
from db_helpers import construct_db_url
from routes import setup_routes


async def init_app():
    app = web.Application()

    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader('templates'),
    )

    setup_routes(app)

    db_url = construct_db_url(user_config)
    await setup_db(db_url)

    redis_pool = await create_pool(
        (user_config.REDIS_HOST, user_config.REDIS_PORT))
    setup_session(app, RedisStorage(redis_pool))

    setup_security(app,
                   SessionIdentityPolicy(),
                   DBAuthorizationPolicy())

    return app


def main():
    logging.basicConfig(level=logging.DEBUG)

    app = init_app()
    web.run_app(app)


if __name__ == '__main__':
    main()
