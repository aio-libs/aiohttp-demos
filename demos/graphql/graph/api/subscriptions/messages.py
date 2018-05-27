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
    message_added = graphene.Field(MessageAdded)

    async def resolve_random_int(self, info: ResolveInfo) -> RandomType:
        i = 0
        while True:
            yield RandomType(seconds=i, random_int=random.randint(0, 500))
            await asyncio.sleep(1.)
            i += 1
