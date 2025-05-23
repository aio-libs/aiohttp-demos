from aiohttp_security.abc import AbstractAuthorizationPolicy

from aiohttpdemo_blog import db
from aiohttpdemo_blog.typedefs import db_key


class DBAuthorizationPolicy(AbstractAuthorizationPolicy):
    def __init__(self, app):
        self.app = app

    async def authorized_userid(self, identity):
        async with self.app[db_key]() as sess:
            user = await db.get_user_by_name(sess, identity)
            if user:
                return identity
        return None

    async def permits(self, identity, permission, context=None):
        if identity is None:
            return False
        return True
