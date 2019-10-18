from graph.utils import APP_PATH
from graph.api.views import (
    GQL,
    subscriptions,
)
from graph.main.views import index


def init_routes(app):
    add_route = app.router.add_route

    add_route('*', '/', index, name='index')
    add_route('*', '/graphql', GQL(), name='graphql')
    add_route('*', '/graphiql', GQL(graphiql=True), name='graphiql')
    add_route('*', '/subscriptions', subscriptions, name='subscriptions')

    # added static dir
    app.router.add_static(
        '/static/',
        path=(APP_PATH / 'static'),
        name='static',
    )
