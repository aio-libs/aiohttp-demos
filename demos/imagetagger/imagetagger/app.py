import asyncio
from pathlib import Path
from typing import Any

import aiohttp_jinja2
import jinja2
from aiohttp import web

from .routes import init_routes
from .utils import init_config, Config, get_config, init_workers
from .views import SiteHandler


path = Path(__file__).parent


def init_jinja2(app: web.Application) -> None:
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(str(path / 'templates'))
    )


async def init_app(conf: Config) -> web.Application:
    app = web.Application()
    executor = await init_workers(app, conf.workers)
    init_config(app, conf)
    init_jinja2(app)
    handler = SiteHandler(conf, executor)
    init_routes(app, handler)
    return app


def main(args: Any = None) -> None:
    conf = get_config(args)
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init_app(conf))
    web.run_app(app, host=conf.app.host, port=conf.app.port)
