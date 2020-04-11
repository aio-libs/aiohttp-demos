# middlewares.py
import aiohttp_jinja2
from aiohttp import web


async def handle_404(request):
    resp = aiohttp_jinja2.render_template('404.html', request, {})
    resp.set_status(404)
    return resp


async def handle_500(request):
    resp = aiohttp_jinja2.render_template('500.html', request, {})
    resp.set_status(500)
    return resp


def create_error_middleware(overrides):

    @web.middleware
    async def error_middleware(request, handler):

        try:
            response = await handler(request)

            override = overrides.get(response.status)
            if override:
                return await override(request)

            return response

        except web.HTTPException as ex:
            override = overrides.get(ex.status)
            if override:
                return await override(request)

            raise

    return error_middleware


def setup_middlewares(app):
    error_middleware = create_error_middleware({
        404: handle_404,
        500: handle_500
    })
    app.middlewares.append(error_middleware)
