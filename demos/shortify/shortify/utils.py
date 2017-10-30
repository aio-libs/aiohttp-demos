import aioredis
import trafaret as t
import yaml
from aiohttp import web


def load_config(fname):
    with open(fname, 'rt') as f:
        data = yaml.load(f)
    # TODO: add config validation
    return data


async def init_redis(conf, loop):
    pool = await aioredis.create_redis_pool(
        (conf['host'], conf['port']),
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
        loop=loop
    )
    return pool


CHARS = "abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def encode(num, alphabet=CHARS):
    if num == 0:
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        num, rem = divmod(num, base)
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)


ShortifyRequest = t.Dict({
    t.Key('url'): t.URL
})


def fetch_url(data):
    try:
        data = ShortifyRequest(data)
    except t.DataError:
        raise web.HTTPBadRequest('URL is not valid')
    return data['url']
