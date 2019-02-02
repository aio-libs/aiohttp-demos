import os
from hashlib import md5

import motor.motor_asyncio as aiomotor
import pytz
import yaml
from aiohttp import web
from dateutil.parser import parse

from . import db


def load_config(fname):
    with open(fname, 'rt') as f:
        data = yaml.load(f)
    # TODO: add config validation
    return data


async def init_mongo(conf, loop):
    host = os.environ.get('DOCKER_MACHINE_IP', '127.0.0.1')
    conf['host'] = host
    mongo_uri = "mongodb://{}:{}".format(conf['host'], conf['port'])
    conn = aiomotor.AsyncIOMotorClient(
        mongo_uri,
        maxPoolSize=conf['max_pool_size'],
        io_loop=loop)
    db_name = conf['database']
    return conn[db_name]


def robo_avatar_url(user_data, size=80):
    """Return the gravatar image for the given email address."""
    hash = md5(str(user_data).strip().lower().encode('utf-8')).hexdigest()
    url = "https://robohash.org/{hash}.png?size={size}x{size}".format(
        hash=hash, size=size)
    return url


def format_datetime(timestamp):
    if isinstance(timestamp, str):
        timestamp = parse(timestamp)
    return timestamp.replace(tzinfo=pytz.utc).strftime('%Y-%m-%d @ %H:%M')


def redirect(request, name, **kw):
    router = request.app.router
    location = router[name].url_for(**kw)
    return web.HTTPFound(location=location)


async def validate_register_form(mongo, form):
    error = None
    user_id = await db.get_user_id(mongo.user, form['username'])

    if not form['username']:
        error = 'You have to enter a username'
    elif not form['email'] or '@' not in form['email']:
        error = 'You have to enter a valid email address'
    elif not form['password']:
        error = 'You have to enter a password'
    elif form['password'] != form['password2']:
        error = 'The two passwords do not match'
    elif user_id is not None:
        error = 'The username is already taken'
    return error
