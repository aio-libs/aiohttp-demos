import logging

import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiohttp_security import SessionIdentityPolicy
from aiohttp_security import authorized_userid
from aiohttp_security import setup as setup_security
from aiohttp_session import setup as setup_session
from aiohttp_session.redis_storage import RedisStorage
from aioredis import create_pool
from aiohttpdemo_blog.db_auth import DBAuthorizationPolicy
from aiohttpdemo_blog.models import init_db
from aiohttpdemo_blog.routes import setup_routes
from aiohttpdemo_blog.settings import load_config, PACKAGE_NAME


log = logging.getLogger(__name__)


async def current_user_ctx_processor(request):
    username = await authorized_userid(request)
    is_anonymous = not bool(username)
    return {'current_user': {'is_anonymous': is_anonymous}}


async def init_app(config):
    app = web.Application()

    app['config'] = config

    setup_routes(app)

    init_db(app)

    redis_pool = await create_pool((
        app['config']['redis']['REDIS_HOST'],
        app['config']['redis']['REDIS_PORT']
    ))
    setup_session(app, RedisStorage(redis_pool))

    # needs to be after session setup because of `current_user_ctx_processor`
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader(PACKAGE_NAME),
        context_processors=[current_user_ctx_processor],
    )

    setup_security(
        app,
        SessionIdentityPolicy(),
        DBAuthorizationPolicy()
    )

    log.debug(app['config'])

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
