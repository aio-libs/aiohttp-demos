import asyncio

import graphene
from graphql.execution.executors.asyncio import AsyncioExecutor
from aiohttp_graphql import GraphQLView

from .queries import Query


gql = GraphQLView(
    schema=graphene.Schema(query=Query),
    # TODO: make global loop
    executor=AsyncioExecutor(loop=asyncio.get_event_loop()),
    graphiql=True,
    enable_async=True,
)
