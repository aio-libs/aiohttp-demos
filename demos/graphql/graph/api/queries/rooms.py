import graphene

from graph.api.models.room import Room
from graph.chat.db_utils import select_rooms


class RoomsQuery(graphene.ObjectType):
    rooms = graphene.List(
        Room,
        description='A list of all available rooms',
    )
    room = graphene.Field(
        Room,
        description='A room object',
    )

    async def resolve_rooms(self, info):
        app = info.context['request'].app

        async with app['db'].acquire() as conn:
            return await select_rooms(conn)
