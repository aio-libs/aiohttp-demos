import bcrypt
import base64
import functools
from enum import Enum

from aiohttp_security.abc import AbstractAuthorizationPolicy
from aiohttp_security import authorized_userid

from . import db


def generate_password_hash(password, salt_rounds=12):
    password_bin = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bin, bcrypt.gensalt(salt_rounds))
    encoded = base64.b64encode(hashed)
    return encoded.decode('utf-8')


def check_password_hash(encoded, password):
    password = password.encode('utf-8')
    encoded = encoded.encode('utf-8')

    hashed = base64.b64decode(encoded)
    is_correct = bcrypt.hashpw(password, hashed) == hashed
    return is_correct


class Permissions(str, Enum):
    view = 'public'
    add = 'private'


class AuthorizationPolicy(AbstractAuthorizationPolicy):
    def __init__(self, mongo):
        self.mongo = mongo

    async def authorized_userid(self, identity):
        # XXX
        return identity

    async def permits(self, identity, permission, context=None):
        if identity is None:
            return False
        return True


async def check_credentials(mongo, username, password):
    user = await self.mongo.user.find_one({'username': form['username']})
    if user and check_password_hash(user['pw_hash'], password):
        return user
    return False


def auth_required(f):
    @functools.wraps(f)
    async def wrapped(self, request):
        user_id = await authorized_userid(request)
        if not user_id:
            raise web.HTTPNotAuthorized()
        return (await f(self, request))
    return wrapped

