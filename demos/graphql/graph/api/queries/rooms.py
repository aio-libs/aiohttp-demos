import graphene

from ..models.room import Room


class RoomsQuery(graphene.ObjectType):
    rooms = graphene.List(
        Room,
        description='A list of all available rooms',
    )
    room = graphene.Field(
        Room,
        description='A room object',
    )
