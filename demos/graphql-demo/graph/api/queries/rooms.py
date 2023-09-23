import graphene
from graphql import ResolveInfo

from graph.api.models.room import Room
from graph.chat.db_utils import select_rooms, select_room


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

    async def resolve_rooms(self, info: ResolveInfo) -> list[list[Room]]:
        app = info.context['request'].app

        async with app['db'].begin() as sess:
            return await select_rooms(sess)

    async def resolve_room(self, info: ResolveInfo, id: int) -> list[Room]:
        app = info.context['request'].app

        async with app['db'].begin() as sess:
            return await select_room(sess, id)
