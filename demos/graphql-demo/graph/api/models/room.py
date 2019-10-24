from typing import List

import graphene
from graphql import ResolveInfo
from aiopg.sa.result import RowProxy

from graph.api.models.user import User
from graph.chat.db_utils import select_messages_by_room_id


__all__ = ['Message', 'Room', ]


class Message(graphene.ObjectType):
    '''
    A messages is main object that representation data of user message.
    '''
    id = graphene.Int(
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

    async def resolve_owner(self, info: ResolveInfo) -> List[RowProxy]:
        app = info.context['request'].app

        return await app['loaders'].users.load(self['owner_id'])


class Room(graphene.ObjectType):
    '''
    A room is point where users can have conversations.
    '''
    id = graphene.Int(
        description="An id of room, it's unique for all rooms",
    )
    name = graphene.String(
        description="A name of room",
    )

    owner = graphene.Field(
        User,
        description='The user who create the current room',
    )
    messages = graphene.List(
        Message,
        description='The messages of the current room',
    )

    async def resolve_owner(self, info: ResolveInfo) -> List[RowProxy]:
        app = info.context['request'].app

        return await app['loaders'].users.load(self['owner_id'])

    async def resolve_messages(self, info: ResolveInfo) -> List[RowProxy]:
        app = info.context['request'].app

        async with app['db'].acquire() as conn:
            return await select_messages_by_room_id(conn, self['id'])
