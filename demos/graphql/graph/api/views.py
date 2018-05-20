import asyncio

import graphene
from graphql.execution.executors.asyncio import AsyncioExecutor
from aiohttp_graphql import GraphQLView

from graph.api.queries import Query


__all__ = ['gql', ]


gql = GraphQLView(
    schema=graphene.Schema(query=Query),
    # TODO: make global loop
    executor=AsyncioExecutor(loop=asyncio.get_event_loop()),
    graphiql=True,
    enable_async=True,
)
