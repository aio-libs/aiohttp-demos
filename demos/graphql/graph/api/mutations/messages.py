import graphene

from graph.auth.db_utils import select_user
from graph.chat.db_utils import (
    create_message,
    delete_message,
)


__all__ = [
    'AddMessageMutation',
    'RemoveMessageMutation',
    'StartTypingMessageMutation',
]


class AddMessageMutation(graphene.Mutation):
    '''
    Gives interface for create new messages.
    '''

    class Arguments:
        room_id = graphene.Int()
        owner_id = graphene.Int()
        body = graphene.String()

    is_created = graphene.Boolean()

    async def mutate(self, info, room_id: int, owner_id: int, body: str):
        app = info.context['request'].app

        async with app['db'].acquire() as conn:
            message = await create_message(conn, room_id, owner_id, body)
            owner = await select_user(conn, owner_id)

        await app['redis_pub'].publish_json(
            f'chat:{room_id}',
            {
                "body": body, "id": message.id,
                "username": owner.username,
                "user_id": owner.id,
            },
        )

        return AddMessageMutation(is_created=True)


class RemoveMessageMutation(graphene.Mutation):
    '''
    Gives interface for create new message by id.
    '''

    class Arguments:
        id = graphene.Int()

    is_removed = graphene.Boolean()

    async def mutate(self, info, id: int):
        app = info.context['request'].app

        async with app['db'].acquire() as conn:
            await delete_message(conn, id)

        return RemoveMessageMutation(is_removed=True)


class StartTypingMessageMutation(graphene.Mutation):
    '''
    Gives interface for set info about start typing new message.
    '''

    class Arguments:
        room_id = graphene.Int()
        user_id = graphene.Int()

    is_success = graphene.Boolean()

    async def mutate(self, info, room_id: int, user_id: int):
        app = info.context['request'].app

        async with app['db'].acquire() as conn:
            user = await select_user(conn, user_id)

        await app['redis_pub'].publish_json(
            f'chat:typing:{room_id}',
            {"username": user.username, "id": user.id},
        )

        return StartTypingMessageMutation(is_success=True)
