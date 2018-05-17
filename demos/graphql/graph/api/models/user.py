import graphene


class User(graphene.ObjectType):
    '''
    A user is an individual's account on current api that can have
    conversations.
    '''
    username = graphene.String(
        description='A username of user',
    )
    email = graphene.String(
        description='A username of user',
    )
