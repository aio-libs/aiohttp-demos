import graphene
from graph.api.models.room import Room
from graph.chat.db_utils import select_room, select_rooms
from graphql import ResolveInfo

__all__ = ("RoomsQuery",)


class RoomsQuery(graphene.ObjectType):
    rooms = graphene.List(
        Room,
        description="A list of all available rooms",
    )
    room = graphene.Field(
        Room,
        id=graphene.Argument(graphene.Int),
        description="A room with given id",
    )

    async def resolve_rooms(self, info: ResolveInfo) -> list[list[Room]]:
        app = info.context["request"].app
        sessionmaker = app["db"]

        try:
            async with sessionmaker() as sess:
                return await select_rooms(sess)
        except Exception as exc:
            raise TypeError(repr(sessionmaker)) from exc

    async def resolve_room(self, info: ResolveInfo, id: int) -> list[Room]:
        app = info.context["request"].app

        async with app["db"]() as sess:
            return await select_room(sess, id)
