import graphene

from graph.chat.db_utils import (
    create_message,
    delete_message,
)


__all__ = ['AddMessageMutation', 'RemoveMessageMutation', ]


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
            await create_message(conn, room_id, owner_id, body)

        await app['redis_pub'].publish_json(f'chat:{room_id}', body)

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
