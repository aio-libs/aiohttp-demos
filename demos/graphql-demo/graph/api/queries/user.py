import graphene

from graph.api.models.user import User


class UserQuery(graphene.ObjectType):
    viewer = graphene.Field(
        User,
        description='A current user',
    )
