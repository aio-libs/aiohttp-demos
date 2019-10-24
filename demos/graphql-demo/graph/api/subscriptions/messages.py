import asyncio
import random

import graphene
from graphql import ResolveInfo

from graph.api.models.user import User


class RandomType(graphene.ObjectType):
    '''
    Random type. Need for test.
    '''
    seconds = graphene.Int()
    random_int = graphene.Int()


class MessageAdded(graphene.ObjectType):
    '''
    The simple type for representation message response in subscription.
    '''
    id = graphene.Int(
        description='The id of message'
    )
    body = graphene.String(
        description='The text of message'
    )
    owner = graphene.Field(
        User,
        description='The owner of current message'
    )


class StartTyping(graphene.ObjectType):
    '''
    The simple type for representation info connected with starting of typing
    new message by some user.
    '''

    user = graphene.Field(
        User,
        description='The user why are typing right now'
    )


class MessageSubscription(graphene.ObjectType):
    '''
    Subscriptions for all actions connected with messages.
    '''
    random_int = graphene.Field(RandomType)
    typing_start = graphene.Field(
        StartTyping,
        room_id=graphene.Argument(graphene.Int)
    )
    message_added = graphene.Field(
        MessageAdded,
        room_id=graphene.Argument(graphene.Int)
    )

    async def resolve_random_int(self, info: ResolveInfo) -> RandomType:
        i = 0
        while True:
            yield RandomType(seconds=i, random_int=random.randint(0, 500))
            await asyncio.sleep(1.)
            i += 1

    async def resolve_message_added(
            self,
            info: ResolveInfo,
            room_id: int,
    ) -> MessageAdded:
        app = info.context['request'].app

        redis = await app['create_redis']()

        res = await redis.subscribe(f'chat:{room_id}')
        ch = res[0]

        while (await ch.wait_message()):
            data = await ch.get_json()
            yield MessageAdded(
                body=data['body'],
                id=data['id'],
                owner=User(id=data['user_id'], username=data['username']),
            )

    async def resolve_typing_start(
            self,
            info: ResolveInfo,
            room_id: int,
    ) -> MessageAdded:
        app = info.context['request'].app

        redis = await app['create_redis']()

        res = await redis.subscribe(f'chat:typing:{room_id}')
        ch = res[0]

        while (await ch.wait_message()):
            data = await ch.get_json()
            yield StartTyping(
                user=User(username=data['username'], id=data['id'])
            )
