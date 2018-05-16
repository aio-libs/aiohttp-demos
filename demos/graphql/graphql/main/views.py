from aiohttp import web

from ..routes import routes


@routes.get('/')
async def index(request: web.Request) -> web.Response:
    return web.Response(body="Hello graphql")
