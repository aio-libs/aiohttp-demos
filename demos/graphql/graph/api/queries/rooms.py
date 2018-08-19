from typing import List

import graphene
from graphql import ResolveInfo
from aiopg.sa.result import RowProxy

from graph.api.models.room import Room
from graph.chat.db_utils import (
    select_rooms,
    select_room,
)


__all__ = ['RoomsQuery', ]


class RoomsQuery(graphene.ObjectType):
    rooms = graphene.List(
        Room,
        description='A list of all available rooms',
    )
    room = graphene.Field(
        Room,
        id=graphene.Argument(graphene.Int),
        description='A room with given id',
    )

    async def resolve_rooms(self, info: ResolveInfo) -> List[RowProxy]:
        app = info.context['request'].app

        async with app['db'].acquire() as conn:
            return await select_rooms(conn)

    async def resolve_room(self, info: ResolveInfo, id: int) -> RowProxy:
        app = info.context['request'].app

        async with app['db'].acquire() as conn:
            return await select_room(conn, id)
