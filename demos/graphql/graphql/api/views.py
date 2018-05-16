from typing import Dict

from aiohttp import web
import aiohttp_jinja2

from ..routes import routes


@routes.get('/graphql')
@aiohttp_jinja2.template('index.jinja2')
async def graph_handler(request: web.Request) -> Dict:
    return {}
