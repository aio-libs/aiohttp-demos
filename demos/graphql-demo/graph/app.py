from functools import partial

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from aiohttp import web
import aioredis
import aiohttp_jinja2
import jinja2

from graph.routes import init_routes
from graph.utils import init_config, APP_PATH
from graph.api.dataloaders import UserDataLoader


def init_jinja2(app: web.Application) -> None:
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(str(APP_PATH / 'templates'))
    )


async def database_ctx(app: web.Application) -> None:
    """This is signal for success creating connection with database."""
    dsn = construct_db_url(app['config']['postgres'])

    engine = create_async_engine(dsn)
    app['db'] = engine

    yield

    await engine.dispose()


def construct_db_url(config) -> str:
    """Construct the database's url from the given config dictionary."""
    DSN = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
    return DSN.format(
        user=config['DB_USER'],
        password=config['DB_PASS'],
        database=config['DB_NAME'],
        host=config['DB_HOST'],
        port=config['DB_PORT'],
    )


async def redis_ctx(app: web.Application) -> None:
    """This is signal for success creating connection with redis."""
    config = app['config']['redis']

    sub = await aioredis.create_redis(
        f'redis://{config["host"]}:{config["port"]}'
    )
    pub = await aioredis.create_redis(
        f'redis://{config["host"]}:{config["port"]}'
    )

    create_redis = partial(
        aioredis.create_redis,
        f'redis://{config["host"]}:{config["port"]}'
    )

    app['redis_sub'] = sub
    app['redis_pub'] = pub
    app['create_redis'] = create_redis

    yield

    app['redis_sub'].close()
    app['redis_pub'].close()


async def init_graph_loaders(app: web.Application) -> None:
    """Initialize data loaders for `graphene`.

    Should be initialized after the database.
    """
    engine = app['db']

    class Loaders:
        users = UserDataLoader(engine, max_batch_size=100)

    app['loaders'] = Loaders()


def init_app() -> web.Application:
    app = web.Application()

    init_jinja2(app)
    init_config(app)
    init_routes(app)

    app.cleanup_ctx.extend((redis_ctx, database_ctx))
    app.on_startup.append(init_graph_loaders)

    return app


async def get_app():
    """Used by aiohttp-devtools for local development."""
    import aiohttp_debugtoolbar
    app = init_app()
    aiohttp_debugtoolbar.setup(app)
    return app
