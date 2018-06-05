from aiohttp_security.abc import AbstractAuthorizationPolicy
from aiohttpdemo_blog.models import User


class DBAuthorizationPolicy(AbstractAuthorizationPolicy):

    async def authorized_userid(self, identity):
        user = await User.query.where(User.username == identity).gino.first()
        if user:
            return identity
        return None

    async def permits(self, identity, permission, context=None):
        if identity is None:
            return False
        return True
