import asyncio

import graphene
from graphql.execution.executors.asyncio import AsyncioExecutor
from aiohttp_graphql import GraphQLView

from graph.api.queries import Query
from graph.api.mutations import Mutation


__all__ = ['GQL', ]


def GQL(graphiql: bool = False) -> GraphQLView:
    '''
    The main view for give access to GraphQl. The view cat work in two modes:

        - simple GraphQl handler
        - GraphIQL view for interactive work with graph application

    :param graphiql: bool
    :return: GraphQLView
    '''

    view = GraphQLView(
        schema=graphene.Schema(
            query=Query,
            mutation=Mutation,
        ),
        # TODO: make global loop
        executor=AsyncioExecutor(loop=asyncio.get_event_loop()),
        graphiql=graphiql,
        enable_async=True,
    )
    return view
