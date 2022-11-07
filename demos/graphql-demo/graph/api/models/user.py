import graphene


__all__ = ['User', ]


class User(graphene.ObjectType):
    """Individual's account on current api that can have conversations."""
    id = graphene.Int(
        description='A id of user',
    )
    username = graphene.String(
        description='A username of user',
    )
    email = graphene.String(
        description='A username of user',
    )
    avatar_url = graphene.String(
        description='A main user`s photo',
    )
