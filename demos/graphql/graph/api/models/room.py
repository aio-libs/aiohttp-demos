import graphene

from ..models.user import User


class Room(graphene.ObjectType):
    '''
    A room is point where users can have conversations.
    '''
    id = graphene.String(
        description="An id of room, it's unique for all rooms",
    )
    name = graphene.String(
        description="A name of room",
    )


class Message(graphene.ObjectType):
    '''
    A messages is main object that representation data of user message.
    '''
    id = graphene.String(
        description="An id of message, it's unique for all message",
    )
    body = graphene.String(
        description="An text of message"
    )
    favouriteCount = graphene.Int(
        description="A count of user who favorited current message",
    )

    owner = graphene.Field(
        User,
        description="An creator of message",
    )
