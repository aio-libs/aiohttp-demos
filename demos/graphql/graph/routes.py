from graph.api.views import GQL
from graph.main.views import index


def init_routes(app):
    add_route = app.router.add_route

    add_route('*', '/', index, name='index')
    add_route('*', '/graphql', GQL(), name='graphql')
    add_route('*', '/graphiql', GQL(graphiql=True), name='graphiql')
