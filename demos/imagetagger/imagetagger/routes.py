import pathlib

from aiohttp import web

from .views import SiteHandler

PROJECT_PATH = pathlib.Path(__file__).parent


def init_routes(app: web.Application, handler: SiteHandler) -> None:
    add_route = app.router.add_route

    add_route('GET', '/', handler.index, name='index')
    add_route('POST', '/predict', handler.predict, name='predict')

    # added static dir
    app.router.add_static(
        '/static/', path=(PROJECT_PATH / 'static'), name='static'
    )
