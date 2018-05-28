import asyncio
import random

import graphene
from graphql import ResolveInfo


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
    text = graphene.String(
        description='The text of message'
    )


class MessageSubscription(graphene.ObjectType):
    '''
    Subscriptions for all actions connected with messages.
    '''
    random_int = graphene.Field(RandomType)
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

        res = await app['redis_sub'].subscribe(f'chat:{room_id}')
        ch = res[0]

        while (await ch.wait_message()):
            msg = await ch.get_json()
            yield MessageAdded(text=msg)
