import graphene

from graph.api.mutations.messages import (
    AddMessage,
    RemoveMessage,
)


class Mutation(graphene.ObjectType):
    '''
    The main GraphQL mutation point.
    '''

    add_message = AddMessage.Field()
    remove_message = RemoveMessage.Field()
