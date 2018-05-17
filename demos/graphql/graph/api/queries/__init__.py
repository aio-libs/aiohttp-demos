from .user import UserQuery
from .rooms import RoomsQuery


class Query(UserQuery, RoomsQuery):
    '''
    The main GraphQL query point.
    '''
