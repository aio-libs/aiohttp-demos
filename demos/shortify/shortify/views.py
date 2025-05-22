import asyncio

import aiohttp_jinja2
from aiohttp import web

from .utils import encode, fetch_url


class SiteHandler:

    def __init__(self, redis, conf):
        self._redis = redis
        self._conf = conf

    @aiohttp_jinja2.template('index.html')
    async def index(self, request):
        return {}

    async def shortify(self, request):
        data = await request.json()
        long_url = fetch_url(data)

        index = await self._redis.incr("shortify:count")
        path = encode(index - 1)
        key = "shortify:{}".format(path)
        await self._redis.set(key, long_url)

        url = "http://{host}:{port}/{path}".format(
            host=self._conf['host'],
            port=self._conf['port'],
            path=path)

        return web.json_response({"url": url})

    async def redirect(self, request):
        short_id = request.match_info['short_id']
        key = 'shortify:{}'.format(short_id)
        location = await self._redis.get(key)
        if not location:
            raise web.HTTPNotFound()
        raise web.HTTPFound(location=location.decode())
