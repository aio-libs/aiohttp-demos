import asyncio

import graphene
from graphql.execution.executors.asyncio import AsyncioExecutor
from aiohttp import web

from graph.api.queries import Query
from graph.api.mutations import Mutation
from graph.api.subscriptions import Subscription
from graph.api.contrib import (
    CustomGraphQLView,
    CustomAiohttpSubscriptionServer,
)


__all__ = ['GQL', 'subscriptions', ]


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription,
)
subscription_server = CustomAiohttpSubscriptionServer(schema)


def GQL(graphiql: bool = False) -> CustomGraphQLView:
    '''
    The main view for give access to GraphQl. The view cat work in two modes:

        - simple GraphQl handler
        - GraphIQL view for interactive work with graph application

    :param graphiql: bool
    :return: GraphQLView
    '''

    view = CustomGraphQLView(
        schema=schema,
        # TODO: make global loop
        executor=AsyncioExecutor(loop=asyncio.get_event_loop()),
        graphiql=graphiql,
        enable_async=True,
        # TODO: remove static url
        # socket="ws://localhost:8080/subscriptions"
        socket="ws://localhost:8080/subscriptions",
    )
    return view


async def subscriptions(request: web.Request) -> web.WebSocketResponse:
    '''
    The handler for creating socket connection with apollo client, for checking
    subscriptions.
    '''
    ws = web.WebSocketResponse(protocols=('graphql-ws',))
    await ws.prepare(request)

    await subscription_server.handle(
        ws,
        request_context={"request": request}
    )

    return ws
