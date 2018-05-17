from .api.views import gql
from .main.views import index


def init_routes(app):
    add_route = app.router.add_route

    add_route('*', '/', index, name='index')
    add_route('*', '/graphiql', gql, name='graphiql')
