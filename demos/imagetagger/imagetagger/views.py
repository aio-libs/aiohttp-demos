import asyncio
from typing import Dict
from concurrent.futures import ProcessPoolExecutor

import aiohttp_jinja2
from aiohttp import web

from .worker import predict
from .utils import Config, executor_key


class SiteHandler:
    def __init__(self, conf: Config, executor: ProcessPoolExecutor) -> None:
        self._conf = conf
        self._executor = executor
        self._loop = asyncio.get_event_loop()

    @aiohttp_jinja2.template('index.html')
    async def index(self, request: web.Request) -> Dict[str, str]:
        return {}

    async def predict(self, request: web.Request) -> web.Response:
        form = await request.post()
        raw_data = form['file'].file.read()
        form["file"].file.close()  # Not needed in aiohttp 4+.
        executor = request.app[executor_key]
        r = self._loop.run_in_executor
        raw_data = await r(executor, predict, raw_data)
        # raw_data = predict(raw_data)
        headers = {'Content-Type': 'application/json'}
        return web.Response(body=raw_data, headers=headers)
