import aiohttp_jinja2
from aiohttp import web

from .utils import CONF_KEY, REDIS_KEY, encode, fetch_url


@aiohttp_jinja2.template('index.html')
async def index(request):
    return {}

async def shortify(request):
    data = await request.json()
    long_url = fetch_url(data)

    conf = request.app[CONF_KEY]
    redis = request.app[REDIS_KEY]
    index = await redis.incr("shortify:count")
    path = encode(index - 1)
    key = "shortify:{}".format(path)
    await redis.set(key, long_url)

    url = "http://{host}:{port}/{path}".format(
        host=conf['host'],
        port=conf['port'],
        path=path)

    return web.json_response({"url": url})

async def redirect(request):
    short_id = request.match_info['short_id']
    key = 'shortify:{}'.format(short_id)
    location = await request.app[REDIS_KEY].get(key)
    if not location:
        raise web.HTTPNotFound()
    raise web.HTTPFound(location=location.decode())
